from rest_framework import serializers
from api.models import Checkpoint
from api.serializers.lane import LaneSerializer
from api.serializers.site import SiteSerializer
from api.serializers.user import UserSerializer


class CheckpointSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    site = SiteSerializer()
    lanes = LaneSerializer(many=True, read_only=True)

    class Meta:
        model = Checkpoint
        fields = "__all__"

