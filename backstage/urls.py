from django.urls import path

from backstage.views import index, ActorListView, ActorDetailView, DirectorListView, GenreListView, PlayListView, DirectorDetailView, PlayDetailView


urlpatterns = [
    path("", index, name="index"),
    path("actors/", ActorListView.as_view(), name="actor-list"),
    path(
        "actors/<int:pk>/", ActorDetailView.as_view(), name="actor-detail"
    ),
    path("directors/", DirectorListView.as_view(), name="director-list"),
    path(
        "directors/<int:pk>/", DirectorDetailView.as_view(), name="director-detail"
    ),
    path("genres/", GenreListView.as_view(), name="genre-list"),
    path("plays/", PlayListView.as_view(), name="play-list"),
    path(
        "plays/<int:pk>/", PlayDetailView.as_view(), name="play-detail"
    )

]

app_name = "backstage"
