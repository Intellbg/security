from rest_framework import serializers
from api.models import LogbookRegister, Person, Checkpoint, QrReader
from datetime import datetime, timedelta


class AccessSerializer(serializers.Serializer):
    username = serializers.CharField()
    SN = serializers.CharField()
    SCode = serializers.CharField()

    def validate_username(self, value):
        checkpoint = Checkpoint.objects.filter(user_username=value).first()
        if not checkpoint:
            raise serializers.ValidationError("Not found")

    def validate_SN(self, value):
        reader = QrReader.objects.filter(sn=value).first()
        if not reader:
            raise serializers.ValidationError("Not found")

    def validate_SCode(self, value):
        hash_mess, identifier = value.split("|$$|")
        if "id" in identifier:
            identifier = identifier.replace("id", "")
            person = Person.objects.get(id=identifier).first()
            if not person:
                raise serializers.ValidationError("Not allowed")
            if person.hash != hash_mess:
                raise serializers.ValidationError("Invalido")
        else:
            lr = LogbookRegister.objects.get(id=identifier).first()
            if not lr:
                raise serializers.ValidationError("Not found")
            if lr.passe_code != hash_mess:
                raise serializers.ValidationError("Invalido")
            if lr.max_entry_time > datetime.now():
                raise serializers.ValidationError("Invalido")
            if lr.entry_time > datetime.now() + timedelta(seconds=60):
                raise serializers.ValidationError("Ya usado")

    def create(self, validated_data):
        return super().create(validated_data)
