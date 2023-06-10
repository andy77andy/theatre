from django.urls import path

from backstage.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "backstage"
