from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('api_v1/imdb/', include("imdb.urls"), name="imdb"),
]
