from .models import CurrencyRate


def convert_amount(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Utility method to conver amount from currenct from_currency to to_currency
    """
    if from_currency == to_currency:
        return amount
    try:

        # return rate
        currency_rate: CurrencyRate = CurrencyRate.objects.get(
            base_currency__code=from_currency, target_currency__code=to_currency
        )

        return amount / float(currency_rate.rate)

    except CurrencyRate.DoesNotExist:
        raise ValueError("Exchange rate not available")
