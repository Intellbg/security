from django.contrib import admin
from .models import (
    Site,
    Administrator,
    Checkpoint,
    Lane,
    QrReader,
    Person,
    LogbookRegister,
    PersonSite,
    Household,
    HouseholdPerson,
)


@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    raw_id_fields = ["user"]
    list_display = ["user", "site"]


@admin.register(Checkpoint)
class CheckpointAdmin(admin.ModelAdmin):
    raw_id_fields = ["user"]
    pass


@admin.register(Lane)
class LaneAdmin(admin.ModelAdmin):
    pass


@admin.register(QrReader)
class QrReaderAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    model = Person
    extra = 1
    fieldsets = (
        (
            "",
            {
                "fields": (
                    "document_number",
                    "id_hash",
                    "celular",
                )
            },
        ),
    )


@admin.register(LogbookRegister)
class LogbookRegisterAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user_host",
        "user_invitee",
        "site",
        "method",
        "address",
        "lane_used",
        "entry_time",
        "passe_active",
    )
    list_filter = (
        "passe_active",
        "site",
        "method",
        "lane_used",
    )
    search_fields = ("user_host__user__email",)
    raw_id_fields = [
        "user_host",
        "user_host",
        "user_invitee",
        "user_invitee",
    ]


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(PersonSite)
class PersonSiteAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "site_approve",
    )
    search_fields = (
        "person__user__email",
        "site__name",
    )
    list_filter = ["site"]
    list_per_page = 1000


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ["address", "site"]
    list_filter = ["site"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(HouseholdPerson)
class HouseholdPersonAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "updated_at"]
    list_display = ["person", "house"]
    list_filter = ["house__site"]
    search_fields = ("person__id",)
    raw_id_fields = ["person"]
