from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from backstage.forms import ActorCreationForm
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


def history(request):

    prev_plays = Play.objects.all().filter(on_stage=False)

    context = {
        "prev_plays": prev_plays,
    }

    return render(request, "backstage/index.html", context=context)


class ActorListView(LoginRequiredMixin, generic.ListView):
    model = Actor
    queryset = (
        Actor.objects.prefetch_related("awards")
    )


class ActorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Actor
    form_class = ActorCreationForm
    success_url = reverse_lazy("backstage:actor-list")


class ActorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Actor
    queryset = Actor.objects.prefetch_related("awards").prefetch_related("plays")


class DirectorListView(LoginRequiredMixin, generic.ListView):
    model = Director


class DirectorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Director
    queryset = Actor.objects.prefetch_related("awards").prefetch_related("plays")


class DirectorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Director
    fields = "__all__"
    success_url = reverse_lazy("backstage:director-list")


class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre


class GenreCreateView(LoginRequiredMixin, generic.CreateView):
    model = Genre
    fields = "__all__"
    success_url = reverse_lazy("backstage:genre-list")


class PlayListView(LoginRequiredMixin, generic.ListView):
    model = Director
    queryset = (
        Play.objects.prefetch_related("awards")
    ).prefetch_related("actors").prefetch_related("directors")


class PlayDetailView(LoginRequiredMixin, generic.DetailView):
    model = Play
    queryset = Actor.objects.prefetch_related("awards").prefetch_related("plays")


class PlayCreateView(LoginRequiredMixin, generic.CreateView):
    model = Award
    fields = "__all__"
    success_url = reverse_lazy("backstage:plays-list")


class AwardListView(LoginRequiredMixin, generic.ListView):
    model = Award


class AwardCreateView(LoginRequiredMixin, generic.CreateView):
    model = Award
    fields = "__all__"
    success_url = reverse_lazy("backstage:plays-list")
