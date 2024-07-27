from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import generics

from api.models import HouseholdPerson
from api.permissions import IsAdministrator
from api.serializers.household_person import (
    HouseholdPersonDetailSerializer,
    HouseholdPersonSerializer,
)


class HouseholdPersonListCreate(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdministrator]
    serializer_class = HouseholdPersonSerializer

    def get_queryset(self):
        site = self.request.user.administrator.first().site
        return HouseholdPerson.objects.filter(house__site=site)


class HouseholdPersonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdministrator]
    serializer_class = HouseholdPersonDetailSerializer

    def get_queryset(self):
        site = self.request.user.administrator.first().site
        return HouseholdPerson.objects.filter(house__site=site)
