from django.urls import include, path
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    path("", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("api/v3/", include("api.urls")),
    path("checkpoint/", include("checkpoint.urls")),
    path("administrator/", include("administrator.urls")),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

