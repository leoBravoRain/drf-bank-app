from rest_framework import serializers
from .models import Transaction 

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user', 'previous_balance', 'new_balance']