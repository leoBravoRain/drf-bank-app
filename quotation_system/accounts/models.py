from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    account_number = models.PositiveIntegerField(unique=True, editable=False)
    currency = models.CharField(max_length=3)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.account_number} - {self.currency} - {self.balance}"
    
