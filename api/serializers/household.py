from rest_framework import serializers
from api.models import Household
from rest_framework.exceptions import PermissionDenied
from rest_framework.validators import UniqueTogetherValidator

class HouseholdMinimumDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = ["address"]

class HouseholdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Household
        fields = [
            "id",
            "address",
            "is_blocked",
            "site",
            "owner"
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Household.objects.all(), fields=["site", "address"]
            )
        ]

    def validate_site(self, value):
        if self.context["request"].user.administrator.first().site != value:
            raise PermissionDenied("Can't create site does not match")
        return value


class HouseholdDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Household
        exclude = ["created_at", "updated_at"]
        read_only_fields = ["site"]

    def validate_address(self, value):
        pk = self.context["request"].parser_context.get("kwargs").get("pk")
        if Household.objects.filter(address=value).exclude(id=pk).exists():
            raise serializers.ValidationError("Already exists")
        return value
