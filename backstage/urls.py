from django.urls import path

from backstage.views import index, ActorListView, ActorDetailView, DirectorListView, GenreListView, PlayListView, \
    DirectorDetailView, PlayDetailView, ActorCreateView, DirectorCreateView, GenreCreateView, history, PlayCreateView, \
    AwardCreateView, AwardListView

urlpatterns = [
    path("", index, name="index"),
    path("actors/", ActorListView.as_view(), name="actor-list"),
    path(
        "actors/<int:pk>/", ActorDetailView.as_view(), name="actor-detail"
    ),
    path("actors/create/", ActorCreateView.as_view(), name="actor-create"),
    path("directors/", DirectorListView.as_view(), name="director-list"),
    path(
        "directors/<int:pk>/", DirectorDetailView.as_view(), name="director-detail"
    ),
    path("directors/create/", DirectorCreateView.as_view(), name="director-create"),
    path("genres/", GenreListView.as_view(), name="genre-list"),
    path("genres/create/", GenreCreateView.as_view(), name="genre-create"),
    path("plays/", PlayListView.as_view(), name="play-list"),
    path("plays/history/", history, name="play-history"),
    path(
        "plays/<int:pk>/", PlayDetailView.as_view(), name="play-detail"
    ),
    path(
        "plays/create/", PlayCreateView.as_view(), name="play-create"
    ),
    path(
        "awards/create/", AwardCreateView.as_view(), name="award-create"
    ),
    path("awards/", AwardListView.as_view(), name="award-list"),
]

app_name = "backstage"
