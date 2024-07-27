from rest_framework import serializers
from api.serializers.person import PersonSerializer
from api.models import LogbookRegister


class LogbookSerializer(serializers.ModelSerializer):
    user_invitee = PersonSerializer(required=False)
    host = serializers.SerializerMethodField("get_host", read_only=True)
    invitee = serializers.SerializerMethodField("get_invitee", read_only=True)
    method = serializers.CharField(source="get_method_display")

    def get_host(self, instance):
        if instance.user_host:
            return str(instance.user_host)
        if not instance.user_host:
            return ""
        return f"{str(instance.user_host.user.first_name)} {str(instance.user_host.user.last_name)}"

    def get_invitee(self, instance):
        if instance.user_invitee:
            return str(instance.user_invitee)
        if not instance.user_invitee:
            return ""
        return f"{str(instance.user_invitee.user.first_name)} {str(instance.user_invitee.user.last_name)}"

    class Meta:
        model = LogbookRegister
        fields = (
            "id",
            "user_host",
            "user_invitee",
            "plate",
            "detail",
            "exit_time",
            "entry_time",
            "host",
            "method",
            "lane_used",
            "invitee",
            "address",
        )
        read_only_fields = ["exit_time", "entry_time", "host", "invitee", "id"]
