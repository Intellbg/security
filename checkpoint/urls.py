from django.urls import path
from .views import index_checkpoint, operations

urlpatterns = [
    path("", index_checkpoint, name="guard_index"),
    path("operations", operations, name="guard_operations"),
]
