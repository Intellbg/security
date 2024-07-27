from django.urls import path
from .views import *

urlpatterns = [
    path('houses',household_table, name='administrator_household_table'),
    path('household-person/create', create_household_person , name='administrator_create_household_person'),
    path('household-details',household_details, name='administrator_household_details'),
    path('household-tags', household_tags_table, name='administrator_household_tags'),
    path('household-persons',household_persons_table, name='administrator_household_persons'),
    path('un-auth-users',pending_authorizations, name='administrator_un_auth_users'),
    path('operations',operations_table, name='administrator_operations'),    
]