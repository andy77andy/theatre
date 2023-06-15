from django.urls import path

from backstage.views import index, ActorListView

urlpatterns = [
    path("", index, name="index"),
    path("actors/", ActorListView.as_view(), name="actor-list"),

]

app_name = "backstage"
