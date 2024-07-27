from rest_framework import serializers

from api.serializers.person import PersonSerializer
from api.serializers.user import UserSerializer
from api.models import Person, PersonSite, Site
from django.db import transaction

class AccountSerializer(serializers.Serializer):
    person = PersonSerializer()
    site = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all())
    user = UserSerializer()

    @transaction.atomic
    def create(self, validated_data):
        user = UserSerializer().create(validated_data=validated_data["user"]) 
        person = Person.objects.create(**validated_data["person"])
        person.user = user
        person.save()
        if validated_data["site"]:
            PersonSite.objects.create(person=person, site=validated_data["site"])
        return validated_data
