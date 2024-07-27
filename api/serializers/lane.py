from api.models import Lane
from rest_framework import serializers


class LaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lane
        exclude = ["checkpoint"]
