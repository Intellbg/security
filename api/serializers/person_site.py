from rest_framework import serializers
from api.serializers.person import PersonDetailSerializer
from api.models import PersonSite


class PersonSiteSerializer(serializers.ModelSerializer):
    person = PersonDetailSerializer()

    class Meta:
        model = PersonSite
        fields = [
            "id",
            "person",
            "site",
            "site_approve",
            "using_passe_id",
            "can_send_external",
            "address",
        ]


class PersonSiteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonSite
        exclude = [
            "person",
            "site",
        ]
