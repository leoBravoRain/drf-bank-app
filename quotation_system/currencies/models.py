from datetime import datetime
from decimal import Decimal

from django.db import models


class Currency(models.Model):
    code: "models.CharField[str, str]" = models.CharField(max_length=3, unique=True)
    name: "models.CharField[str, str]" = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.code} - {self.name}"


class CurrencyRate(models.Model):
    base_currency: models.ForeignKey[Currency, Currency] = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="base_rates"
    )
    target_currency: models.ForeignKey[Currency, Currency] = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="target_rates"
    )
    rate: "models.DecimalField[Decimal, Decimal]" = models.DecimalField(
        max_digits=12, decimal_places=6
    )
    last_updated: "models.DateTimeField[datetime, datetime]" = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = ("base_currency", "target_currency")

    def __str__(self):
        return f"1 {self.base_currency.code} = {self.rate} {self.target_currency.code}"
