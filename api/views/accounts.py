
from api.serializers.accounts import AccountSerializer
from rest_framework import generics


class AccountsCreateView(generics.CreateAPIView):
    serializer_class = AccountSerializer
