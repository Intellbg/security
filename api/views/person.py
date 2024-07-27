from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAdministrator

from api.models import Person
from api.serializers.person import PersonDetailSerializer

class PersonDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdministrator]
    queryset = Person.objects.all()
    serializer_class = PersonDetailSerializer
