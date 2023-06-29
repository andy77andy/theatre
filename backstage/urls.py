from django.urls import path

from backstage.views import index, ActorListView, ActorDetailView, DirectorListView, GenreListView, PlayListView, \
    DirectorDetailView, PlayDetailView, ActorCreateView, DirectorCreateView, GenreCreateView, history, PlayCreateView, \
    AwardCreateView, AwardListView, DirectorUpdateView, ActorUpdateView, GenreUpdateView, PlayUpdateView, \
    AwardUpdateView, ActorDeleteView, DirectorDeleteView, GenreDeleteView, PlayDeleteView, AwardDeleteView

urlpatterns = [
    path("", index, name="index"),
    path("actors/", ActorListView.as_view(), name="actor-list"),
    path(
        "actors/<int:pk>/", ActorDetailView.as_view(), name="actor-detail"
    ),
    path("actors/create/", ActorCreateView.as_view(), name="actor-create"),
    path("actors/<int:pk>/update/", ActorUpdateView.as_view(), name="actor-update"),
    path("actors/<int:pk>/delete/", ActorDeleteView.as_view(), name="actor-delete"),
    path("directors/", DirectorListView.as_view(), name="director-list"),
    path(
        "directors/<int:pk>/", DirectorDetailView.as_view(), name="director-detail"
    ),
    path("directors/create/", DirectorCreateView.as_view(), name="director-create"),
    path("directors/<int:pk>/update/", DirectorUpdateView.as_view(), name="director-update"),
    path("directors/<int:pk>/delete/", DirectorDeleteView.as_view(), name="director-delete"),
    path("genres/", GenreListView.as_view(), name="genre-list"),
    path("genres/create/", GenreCreateView.as_view(), name="genre-create"),
    path("genres/<int:pk>/update/", GenreUpdateView.as_view(), name="genre-update"),
    path("genres/<int:pk>/delete/", GenreDeleteView.as_view(), name="genre-delete"),
    path("plays/", PlayListView.as_view(), name="play-list"),
    path("plays/upcoming/", PlayListView.as_view(), name="play-upcoming"),
    path("plays/archive/", PlayListView.as_view(), name="play-archive"),
    path(
        "plays/<int:pk>/", PlayDetailView.as_view(), name="play-detail"
    ),
    path(
        "plays/create/", PlayCreateView.as_view(), name="play-create"
    ),
    path("plays/<int:pk>/update/", PlayUpdateView.as_view(), name="play-update"),
    path("plays/<int:pk>/delete/", PlayDeleteView.as_view(), name="play-delete"),
    path(
        "awards/create/", AwardCreateView.as_view(), name="award-create"
    ),
    path("awards/", AwardListView.as_view(), name="award-list"),
    path("awards/<int:pk>/update/", AwardUpdateView.as_view(), name="award-update"),
    path("awards/<int:pk>/delete/", AwardDeleteView.as_view(), name="award-delete"),
]

app_name = "backstage"
