from django.shortcuts import render
from rest_framework import generics
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework import permissions
from rest_framework import serializers
from quotation_system.accounts.models import Account
from django.db import transaction
from ..currencies.utils import convert_amount

class TransactionListView(generics.ListCreateAPIView):
    """
    List all transactions for a user.
    Create a new transaction for a user.
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        
        user = self.request.user
        transaction_type = self.request.data['transaction_type']
        
        # add user to the transaction serializer
        serializer.validated_data['user'] = user
        
        trx_amount = serializer.validated_data['amount']
        
        with transaction.atomic():
            
            # get account to update balnace
            # ^ select_for_update() locks the row to avoid race conditions in concurrent transactions
            account = Account.objects.select_for_update().get(user=user, pk=self.request.data['account'])
            
            # update balance
            # --- DEPOSIT ----
            if transaction_type == Transaction.TRANSACTION_TYPES[0][0]:
                
                # convert amount 
                converted_amount = convert_amount(trx_amount, serializer.validated_data['currency'], account.currency)
                
                # update transaction previous
                serializer.validated_data['previous_balance'] = account.balance
                
                # update account balance
                account.balance += converted_amount
                
                # update transaction new balance
                serializer.validated_data['new_balance'] = account.balance
                
            # --- WITHDRAWAL ----
            elif transaction_type == Transaction.TRANSACTION_TYPES[1][0]:
                
                
                # convert amount 
                converted_amount = convert_amount(trx_amount, serializer.validated_data['currency'], account.currency)
                
                # check if account has enough balance
                if account.balance < converted_amount:
                    raise serializers.ValidationError("Insufficient balance")
                
                # update transaction previous and new balance
                serializer.validated_data['previous_balance'] = account.balance 
                
                # update account balance
                account.balance -= converted_amount
                
                # update transaction new balance
                serializer.validated_data['new_balance'] = account.balance
                
            # --- TRANSFER ----
            elif transaction_type == Transaction.TRANSACTION_TYPES[2][0]:
                
                # check if related_account is defined
                if not self.request.data.get('related_account'):
                    raise serializers.ValidationError("Related account must be defined")
                
                # get receiver account
                receiver_account = Account.objects.select_for_update().get(user=user, pk=self.request.data['related_account'])
                
                # check if sender account has enough balance
                if account.balance < serializer.validated_data['amount']:
                    raise serializers.ValidationError("Insufficient balance")
                
                # update transaction previous and new balance
                serializer.validated_data['previous_balance'] = account.balance 
                
                # update account balance
                account.balance -= serializer.validated_data['amount']
                
                # convert amount to receiver currency
                receiver_converted_amount = convert_amount(trx_amount, account.currency, receiver_account.currency)
                
                # update receiver account balance
                receiver_account.balance += receiver_converted_amount
                
                # update transaction new balance
                serializer.validated_data['new_balance'] = account.balance
                
                # set currency as the sender currency
                serializer.validated_data['currency'] = account.currency
                
                
            else:
                raise serializers.ValidationError("Invalid transaction type")
            
            # save account
            account.save()

            # create transaction
            serializer.save()
            
            # update receviver 
            if transaction_type == Transaction.TRANSACTION_TYPES[2][0]:
                receiver_account.save()
class TransactionDetailView(generics.RetrieveAPIView):
    
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return Transaction.objects.get(user=self.request.user, pk=self.kwargs['pk'])
        
        
        
        
        
        

