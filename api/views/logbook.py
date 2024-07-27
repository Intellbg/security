from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import generics

from api.filters import LogbookFilter
from api.models import LogbookRegister
from api.serializers.logbook import LogbookSerializer

from api.permissions import IsAdministrator, IsCheckpoint


def get_query(self):
    qs = LogbookRegister.objects.filter(
        entry_time__isnull=False,
    ).order_by("-entry_time")
    if self.request.user.administrator.first():
        return qs.filter(site=self.request.user.administrator.first().site)
    if self.request.user.checkpoint.first():
        return qs.filter(site=self.request.user.checkpoint.first().site)
    return None


class LogbookList(generics.ListAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdministrator | IsCheckpoint]
    serializer_class = LogbookSerializer
    filterset_class = LogbookFilter

    def get_queryset(self):
        return get_query(self)


class LogbookViewDetail(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdministrator | IsCheckpoint]
    serializer_class = LogbookSerializer

    def get_queryset(self):
        return get_query(self)
