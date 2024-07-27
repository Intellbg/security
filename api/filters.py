from api.models import LogbookRegister, Household
import django_filters

class LogbookFilter(django_filters.FilterSet):
    class Meta:
        model = LogbookRegister
        fields = {
            "entry_time": ["lt", "gt", "gte", "lte"],
            "user_invitee__first_name": [
                "exact",
                "contains",
                "icontains",
                "istartswith",
            ],
            "user_invitee__last_name": [
                "exact",
                "contains",
                "icontains",
                "istartswith",
            ],
            "user_invitee__document_number": ["istartswith"],
            "user_host__last_name": [
                "exact",
                "icontains",
                "contains",
                "istartswith",
            ],
            "user_host__first_name": [
                "exact",
                "contains",
                "icontains",
                "istartswith",
            ],
            "plate": ["contains", "istartswith"],
        }


class HouseholdFilter(django_filters.FilterSet):
    class Meta:
        model = Household
        fields = {
            'address': ['istartswith', 'exact'],
        }