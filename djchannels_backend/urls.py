from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/chatapp/", include("chatapp.urls")),
    path("api/account/", include("account.urls")),
    path("api/genchatapp/", include("genchatapp.urls")),
]

urlpatterns += [re_path(r"^.*", TemplateView.as_view(template_name="index.html"))]
