from .models import CurrencyRate

def convert_amount(amount, from_currency, to_currency):
    """
    Utility method to conver amount from currenct from_currency to to_currency
    """    
    if from_currency == to_currency:
        amount
    try:
        # return rate
        rate = CurrencyRate.objects.get(
            base_currency = from_currency,
            target_currency = to_currency
        ).rate
        
        return amount*rate
        
    except CurrencyRate.DoesNotExist:
        raise ValueError('Exchange rate not available')