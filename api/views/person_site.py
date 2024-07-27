from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from api.models import PersonSite
from api.permissions import IsAdministrator
from api.serializers.person_site import (
    PersonSiteDetailSerializer,
    PersonSiteSerializer,
)


class PersonSiteListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdministrator]
    queryset = PersonSite.objects.all()
    serializer_class = PersonSiteSerializer
    filterset_fields = ['site_approve']


class PersonSiteDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdministrator]
    queryset = PersonSite.objects.all()
    serializer_class = PersonSiteDetailSerializer
