from django.shortcuts import render
from rest_framework import generics
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework import permissions
from rest_framework import serializers
from quotation_system.accounts.models import Account

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
        
        # get account to update balnace
        account = Account.objects.get(user=user, pk=self.request.data['account'])
        
        # update balance
        # if it's a deposit
        if transaction_type == Transaction.TRANSACTION_TYPES[0][0]:
            
            # update transaction previous
            serializer.validated_data['previous_balance'] = account.balance
            
            # update account balance
            account.balance += serializer.validated_data['amount']
            
            # update transaction new balance
            serializer.validated_data['new_balance'] = account.balance
            
        # if it's a withdrawal, decrease balance
        elif transaction_type == Transaction.TRANSACTION_TYPES[1][0]:
            
            # check if account has enough balance
            if account.balance < serializer.validated_data['amount']:
                raise serializers.ValidationError("Insufficient balance")
            
            # update transaction previous and new balance
            serializer.validated_data['previous_balance'] = account.balance 
            
            # update account balance
            account.balance -= serializer.validated_data['amount']
            
            # update transaction new balance
            serializer.validated_data['new_balance'] = account.balance
            
        # transfer funds to another account
        elif transaction_type == Transaction.TRANSACTION_TYPES[2][0]:
            
            # check if related_account is defined
            if not self.request.data['related_account']:
                raise serializers.ValidationError(f"Related account must be defined in a ${transaction_type} transaction. This is the receiver account.")
            
            # get receiver account
            receiver_account = Account.objects.get(user=user, pk=self.request.data['related_account'])
            
            # check if sender account has enough balance
            if account.balance < serializer.validated_data['amount']:
                raise serializers.ValidationError("Insufficient balance")
            
            # update transaction previous and new balance
            serializer.validated_data['previous_balance'] = account.balance 
            
            # update account balance
            account.balance -= serializer.validated_data['amount']
            
            # update receiver account balance
            receiver_account.balance += serializer.validated_data['amount']
            
            # update transaction new balance
            serializer.validated_data['new_balance'] = account.balance
            
            
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
        
        
        
        
        
        

