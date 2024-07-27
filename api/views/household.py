from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.models import Household
from api.serializers.household import (
    HouseholdDetailSerializer,
    HouseholdSerializer,
)
from api.permissions import IsAdministrator
from api.filters import HouseholdFilter


class HouseholdListCreate(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdministrator]
    serializer_class = HouseholdSerializer
    filterset_class = HouseholdFilter

    def get_queryset(self):
        site = self.request.user.administrator.first().site
        return Household.objects.filter(site=site)


class HouseholdRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdministrator]
    serializer_class = HouseholdDetailSerializer

    def get_queryset(self):
        site = self.request.user.administrator.first().site
        return Household.objects.filter(site=site)
