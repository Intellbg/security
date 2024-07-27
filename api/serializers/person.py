from rest_framework import serializers
from api.models import Person
from .user import UserSerializer
import uuid


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["document_number", "last_name", "first_name", "celular"]
        read_only = ['celular']
        extra_kwargs = {
            "document_number": {"required": True},
            "last_name": {"required": True},
            "first_name": {"required": True},
        }


class PersonDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Person
        fields = ("id", "last_name", "first_name", "document_number", "celular", "user")

    def validate_document_number(self, attrs):
        if attrs == "":
            attrs = uuid.uuid4()
        if (
            Person.objects.filter(document_number=attrs)
            .exclude(id=self.instance.id)
            .exists()
        ):
            raise serializers.ValidationError(
                "Ya existe una persona con ese número de documento"
            )
        return attrs
