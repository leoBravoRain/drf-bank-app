from django.shortcuts import render
from rest_framework import generics
from .models import Account
from .serializers import AccountSerializer
from rest_framework import permissions

class CreateAccountView(generics.CreateAPIView):
    """
    Create a new account for a user.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, balance=0)