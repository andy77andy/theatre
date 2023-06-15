from django.urls import path

from backstage.views import index, ActorListView, ActorDetailView

urlpatterns = [
    path("", index, name="index"),
    path("actors/", ActorListView.as_view(), name="actor-list"),
    path(
        "actors/<int:pk>/", ActorDetailView.as_view(), name="actor-detail"
    ),

]

app_name = "backstage"
