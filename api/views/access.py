from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from api.permissions import IsCheckpoint
from api.serializers.access import AccessSerializer
from rest_framework import generics
import logging
logger = logging.getLogger("checkpoint")
from django_project.utils import get_client_ip

class AccessCreateView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsCheckpoint]
    serializer_class = AccessSerializer

    def post(self, request, *args, **kwargs):
        obj = self.create(request, *args, **kwargs)
        logger.info(f"{get_client_ip(self.context.get('request'))} {obj.id} Access conced")
        return obj