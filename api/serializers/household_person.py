import re
from rest_framework import serializers
from api.serializers.household import HouseholdMinimumDetailSerializer
from api.models import HouseholdPerson, Person
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Q
from api.serializers.person import PersonSerializer


class HouseholdPersonSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    house_detail = HouseholdMinimumDetailSerializer(
        source="house",
        read_only=True,
    )

    class Meta:
        model = HouseholdPerson
        exclude = ["created_at", "updated_at"]
        validators = [
            UniqueTogetherValidator(
                queryset=HouseholdPerson.objects.all(), fields=["person", "house"]
            )
        ]

    def validate_house(self, value):
        if self.context["request"].user.administrator.first().site != value.site:
            raise serializers.ValidationError("Can't create site does not match")
        return value

    def validate_person(self, attrs):
        attrs["document_number"] = re.sub("[^0-9a-zA-Z\s]+", "", attrs["document_number"]).upper()
        document_number = attrs["document_number"]
        person_query = Person.objects.filter(
            Q(document_number=document_number) 
        ).exclude(document_number__isnull=True).exclude(document_number="")
        if person_query:
            person = person_query.first()
        else:
            if not attrs['document_number']:
                attrs.pop("document_number")
            person = Person.objects.create(**attrs)
        return person


class HouseholdPersonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseholdPerson
        exclude = ["created_at", "updated_at"]
        validators = [
            UniqueTogetherValidator(
                queryset=HouseholdPerson.objects.all(), fields=["person", "house"]
            )
        ]
        read_only_fields = ["person", "house"]
