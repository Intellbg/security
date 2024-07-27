from django.urls import path
from rest_framework.authtoken import views

from api.views.access import AccessCreateView
from api.views.checkpoint import CheckpointView
from api.views.household import HouseholdListCreate, HouseholdRetrieveUpdateDelete
from api.views.logbook import LogbookList, LogbookViewDetail
from api.views.person import PersonDetailView
from api.views.person_site import PersonSiteDetailView, PersonSiteListView
from api.views.accounts import AccountsCreateView
from .views.household_person import HouseholdPersonListCreate, HouseholdPersonRetrieveUpdateDestroy 

urlpatterns = [
    path("accounts/api-token-auth/", views.obtain_auth_token),
    
    path("account", AccountsCreateView.as_view(), name="account_create"),

    path("checkpoint", CheckpointView.as_view(), name="checkpoint"),

    path("check-qr", AccessCreateView.as_view(), name="check_qr"),

    path("person/<int:pk>", PersonDetailView.as_view(), name="person_detail"),

    path("person-site/", PersonSiteListView.as_view(), name="person_site"),
    path("person-site/<int:pk>/", PersonSiteDetailView.as_view(),name="person_site_detail"),

    path("logbook-register", LogbookList.as_view(), name="logbook_register"),
    path("logbook-register/<int:pk>", LogbookViewDetail.as_view(), name="logbook_register_detail"),
    
    path("households/", HouseholdListCreate.as_view(), name="api_v3_households"),
    path("households/<int:pk>/", HouseholdRetrieveUpdateDelete.as_view(), name="api_v3_households_detail"),
    
    path("household-person/", HouseholdPersonListCreate.as_view(), name="api_v3_household_person"),
    path("household-person/<int:pk>/", HouseholdPersonRetrieveUpdateDestroy.as_view(), name="api_v3_household_person_detail"),
]
