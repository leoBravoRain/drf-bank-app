from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    account_number = models.PositiveIntegerField(unique=True, editable=False)
    currency = models.CharField(max_length=3)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # only when creating a new account
        if not self.account_number:
            last_account = Account.objects.order_by("-account_number").first()
            if last_account:
                self.account_number = last_account.account_number + 1
            else:
                self.account_number = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.account_number} - {self.currency} - {self.balance}"
