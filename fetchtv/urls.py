from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('api_v1/omdb/', include("omdb.urls"), name="omdb"),
]
