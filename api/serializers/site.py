
from api.models import Site
from rest_framework import serializers

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = [
            "id",
            "name",
            "address",
            "max_entry_time",
            "has_passe_id",
            "has_qr_down",
        ]
