from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic

from backstage.models import Award, Actor, Director, Play, Genre


# @login_required
def index(request):

    num_actors = Actor.objects.count()
    num_directors = Director.objects.count()
    num_plays = Play.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_actors": num_actors,
        "num_directors": num_directors,
        "num_plays": num_plays,
        "num_visits": num_visits + 1,
    }

    return render(request, "backstage/index.html", context=context)


class ActorListView(generic.ListView):
    model = Actor
    queryset = (
        Actor.objects.prefetch_related("awards")
    )


class ActorDetailView(generic.DetailView):
    model = Actor
    queryset = Actor.objects.prefetch_related("awards")
        # prefetch_related("play__actors")


class DirectorListView(generic.ListView):
    model = Director
    queryset = (
        Director.objects.prefetch_related("awards")
    )


class GenreListView(generic.ListView):
    model = Genre


class PlayListView(generic.ListView):
    model = Director
    queryset = (
        Play.objects.prefetch_related("awards")
    ).prefetch_related("actors").prefetch_related("directors")
