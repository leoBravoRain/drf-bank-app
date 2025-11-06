from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Account
        fields = '__all__'