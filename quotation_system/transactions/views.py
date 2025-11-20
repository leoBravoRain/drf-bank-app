import structlog
from django.core.cache import cache
from django.db import transaction
from django.utils.encoding import force_str
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response

from quotation_system.accounts.models import Account

from ..currencies.utils import convert_amount
from .filters import TransactionFilter
from .models import Transaction
from .paginator import TransactionsPaginator
from .serializers import TransactionSerializer

logger = structlog.get_logger()


class TransactionListView(generics.ListCreateAPIView):
    """
    List all transactions for a user.
    Create a new transaction for a user.
    """

    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter
    pagination_class = TransactionsPaginator

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )

    def list(self, request, *args, **kwargs):

        user_id = self.request.user.id

        # Build cache key. Include query params so pagination + filters work.
        query_params = force_str(self.request.query_params.urlencode())
        cache_key = f"user:{user_id}:transactions:{query_params}"

        # try to get cached data
        cached_data = cache.get(cache_key)

        # if cached data, return it
        if cached_data:
            logger.info("Returning cached transactions")
            return Response(cached_data)

        # Otherwise normal DRF behaviour
        response = super().list(request, *args, **kwargs)

        logger.info("Caching query response")
        # cache evaluated list
        result = response.data

        cache.set(cache_key, result, timeout=60)

        return response

    def perform_create(self, serializer):

        logger.info("trying to create a new trx with params")

        user = self.request.user
        transaction_type = self.request.data["transaction_type"]

        # add user to the transaction serializer
        serializer.validated_data["user"] = user

        trx_amount = serializer.validated_data["amount"]

        with transaction.atomic():

            # get account to update balnace
            # ^ select_for_update() locks the row to avoid race conditions in concurrent transactions
            account = Account.objects.select_for_update().get(
                user=user, pk=self.request.data["account"]
            )

            # update balance
            # --- DEPOSIT ----
            if transaction_type == Transaction.TRANSACTION_TYPES[0][0]:

                # convert amount
                converted_amount = convert_amount(
                    trx_amount, serializer.validated_data["currency"], account.currency
                )

                # update transaction previous
                serializer.validated_data["previous_balance"] = account.balance

                # update account balance
                account.balance += converted_amount

                # update transaction new balance
                serializer.validated_data["new_balance"] = account.balance

            # --- WITHDRAWAL ----
            elif transaction_type == Transaction.TRANSACTION_TYPES[1][0]:

                # convert amount
                converted_amount = convert_amount(
                    trx_amount, serializer.validated_data["currency"], account.currency
                )

                # check if account has enough balance
                if account.balance < converted_amount:
                    raise serializers.ValidationError("Insufficient balance")

                # update transaction previous and new balance
                serializer.validated_data["previous_balance"] = account.balance

                # update account balance
                account.balance -= converted_amount

                # update transaction new balance
                serializer.validated_data["new_balance"] = account.balance

            # --- TRANSFER ----
            elif transaction_type == Transaction.TRANSACTION_TYPES[2][0]:

                # check if related_account is defined
                if not self.request.data.get("related_account"):
                    raise serializers.ValidationError("Related account must be defined")

                # get receiver account
                receiver_account = Account.objects.select_for_update().get(
                    user=user, pk=self.request.data["related_account"]
                )

                # check if sender account has enough balance
                if account.balance < serializer.validated_data["amount"]:
                    raise serializers.ValidationError("Insufficient balance")

                # update transaction previous and new balance
                serializer.validated_data["previous_balance"] = account.balance

                # update account balance
                account.balance -= serializer.validated_data["amount"]

                # convert amount to receiver currency
                receiver_converted_amount = convert_amount(
                    trx_amount, account.currency, receiver_account.currency
                )

                # update receiver account balance
                receiver_account.balance += receiver_converted_amount

                # update transaction new balance
                serializer.validated_data["new_balance"] = account.balance

                # set currency as the sender currency
                serializer.validated_data["currency"] = account.currency

            else:
                raise serializers.ValidationError("Invalid transaction type")

            # save account
            account.save()

            # create transaction
            serializer.save()

            # update receviver
            if transaction_type == Transaction.TRANSACTION_TYPES[2][0]:
                receiver_account.save()

        # Invalidate all cached transaction lists for this user
        self.invalidate_user_cache(self.request.user.id)

    def invalidate_user_cache(self, user_id: int):
        """
        Remove ALL keys related to transaction list for this user.
        Example keys:
            user:7:transactions:
            user:7:transactions?page=2
            user:7:transactions?type=DEBIT
        """
        pattern = f"user:{user_id}:transactions:*"
        keys = cache.keys(pattern)
        if keys:
            cache.delete_many(keys)


class TransactionDetailView(generics.RetrieveAPIView):

    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Transaction.objects.get(user=self.request.user, pk=self.kwargs["pk"])
