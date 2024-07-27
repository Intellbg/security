import uuid
from django.db import models
from django.contrib.auth.models import User
from django_project.hasher import generate_hash
from django.template.loader import render_to_string
from datetime import datetime
from django_project.pusher import pusher_client


class Site(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=140)
    address = models.CharField(max_length=300, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    max_entry_time = models.IntegerField(default=5)
    has_passe_id = models.BooleanField(default=True)
    has_qr_down = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Administrator(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="administrator"
    )
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.email


class Checkpoint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="checkpoint")
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_pusher_channel(self):
        return "private-guard-check_operation_" + self.user

    def send_pusher_notification(self, error=None, operation=None):
        context = {"status": 200}
        if error:
            context = {"error": error, "status": 400, "datetime": datetime.now()}
        if operation:
            context["field"] = operation
        template = render_to_string("code_check.html", context)
        pusher_client.trigger(
            self.get_pusher_channel(), "check-code", {"html": template}
        )


class Person(models.Model):

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    document_number = models.CharField(
        max_length=36, blank=True, null=True, default=uuid.uuid4
    )
    celular = models.CharField(max_length=13, null=True, blank=True)
    id_hash = models.CharField(default=generate_hash, max_length=140)
    creation_time = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="person"
    )

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"

    def __str__(self):
        return f"{self.first_name or '' } {self.last_name or'' }"


class PersonSite(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, related_name="sites", on_delete=models.CASCADE)
    site = models.ForeignKey(Site, related_name="persons", on_delete=models.CASCADE)
    site_approve = models.BooleanField(default=False)
    using_passe_id = models.BooleanField(default=False)
    can_send_external = models.BooleanField(default=False)
    address = models.CharField(max_length=200, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person.user.email} / {self.site.name}"


class Household(models.Model):
    address = models.CharField(max_length=100)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="site_houses")
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["address"]

    @property
    def owner(self):
        return (
            HouseholdPerson.objects.filter(
                house=self.id, relation=HouseholdPerson.OWNER
            )
            .first()
            .person.id
        )


class HouseholdPerson(models.Model):
    OWNER = "O"
    COUPLE = "C"
    CHILDREN = "CR"
    RELATIVE = "R"
    FRIEND = "F"
    TENANT = "T"
    OTHER = "OT"
    RELATION_CHOICES = (
        (OWNER, "owner"),
        (COUPLE, "couple"),
        (CHILDREN, "children"),
        (RELATIVE, "relative"),
        (FRIEND, "friend"),
        (TENANT, "tenant"),
        (OTHER, "other"),
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="person_houses"
    )
    house = models.ForeignKey(
        Household, on_delete=models.CASCADE, related_name="people"
    )
    relation = models.CharField(
        max_length=2,
        choices=RELATION_CHOICES,
        default=OWNER,
    )
    is_blocked = models.BooleanField(default=False)

    can_use_passe_id = models.BooleanField(default=True)
    can_send_invitations = models.BooleanField(default=True)
    can_send_external = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LogbookRegister(models.Model):
    PASSE_ID = "ID"
    PASSE_INVITATION = "I"
    PASSE_INVITATION_DOWNLOAD = "D"
    METHOD = (
        (PASSE_ID, "Passe ID"),
        (PASSE_INVITATION, "Invitación"),
        (PASSE_INVITATION_DOWNLOAD, "Invitación Descargada"),
    )

    id = models.AutoField(primary_key=True)
    user_host = models.ForeignKey(
        Person, related_name="host", blank=True, null=True, on_delete=models.CASCADE
    )
    user_invitee = models.ForeignKey(
        Person,
        related_name="invitee",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    site = models.ForeignKey(
        Site,
        related_name="site",
        on_delete=models.CASCADE,
    )
    creation_time = models.DateTimeField(auto_now_add=True)
    entry_time = models.DateTimeField(blank=True, null=True)
    max_entry_time = models.DateTimeField(blank=True, null=True)
    passe_active = models.BooleanField(default=True)
    passe_code = models.CharField(max_length=140, default=generate_hash)
    plate = models.CharField(max_length=20, blank=True, null=True)
    method = models.CharField(max_length=2, blank=True, null=True, choices=METHOD)
    address = models.CharField(max_length=100, blank=True, null=True)
    lane_used = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user_host.user.get_username() + " invita USUARIO_NO_REGISTRADO"


class Lane(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    checkpoint = models.ForeignKey(
        Checkpoint, on_delete=models.CASCADE, related_name="lanes"
    )

    def __str__(self):
        return f"{self.name} | {self.checkpoint}"


class QrReader(models.Model):
    sn = models.CharField(max_length=50)
    lane = models.ForeignKey(
        Lane,
        on_delete=models.CASCADE,
        related_name="lane_reader",
        null=True,
        blank=True,
    )
    allow_passe_id = models.BooleanField(default=True)
    allow_passe_invitation = models.BooleanField(default=True)

    def __str__(self):
        return f"QR reader {self.lane}"

    def get_invalid_response_data(self, message):
        return {"Msg": message, "ResultCode": 0, "ActIndex": 1, "Audio": 25}

    def get_valid_response_data(self):
        return {"Msg": "Bienvenido", "ResultCode": 1, "ActIndex": 1, "Audio": 26}
