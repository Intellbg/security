from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from api.permissions import IsCheckpoint
from api.models import Checkpoint
from api.serializers.checkpoint import CheckpointSerializer
from rest_framework import generics


class CheckpointView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsCheckpoint]
    serializer_class = CheckpointSerializer

    def get_queryset(self):
        return Checkpoint.objects.filter(user=self.request.user)
