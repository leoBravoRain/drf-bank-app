from rest_framework import serializers
from .models import Currency, CurrencyRate

class CurrencySerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Currency
        fields = '__all__'
        
class CurrencyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyRate
        fields = '__all__'