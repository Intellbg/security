from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from api.permissions import IsCheckpoint
from api.serializers.access import AccessSerializer
from rest_framework import generics


class AccessCreateView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsCheckpoint]
    serializer_class = AccessSerializer
