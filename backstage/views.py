from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from backstage.forms import ActorCreationForm, ActorValidateUpdateDataForm, PlayForm, PlaySearchForm, ActorSearchForm
# CombinedPlayForm
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

    prev_plays = Play.objects.filter(on_stage=False)

    context = {
        "prev_plays": prev_plays,
    }

    return render(request, "backstage/index.html", context=context)


class ActorListView(LoginRequiredMixin, generic.ListView):
    model = Actor
    queryset = (
        Actor.objects.prefetch_related("awards")
    )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ActorListView, self).get_context_data(**kwargs)
        context["search"] = ActorSearchForm()

        last_name = self.request.GET.get("last_name", "")

        context["search"] = ActorSearchForm(
            initial={"last_name": last_name}
        )

        return context

    def get_queryset(self) -> QuerySet:
        queryset = (
            Actor.objects.prefetch_related("awards")
        )
        form = ActorSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(last_name__icontains=form.cleaned_data["last_name"])
        return queryset


class ActorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Actor
    form_class = ActorCreationForm
    success_url = reverse_lazy("backstage:actor-list")


class ActorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Actor
    queryset = Actor.objects.prefetch_related("awards").prefetch_related("plays")


class ActorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Actor
    form_class = ActorValidateUpdateDataForm
    success_url = reverse_lazy("backstage:actor-list")


class ActorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Actor
    success_url = reverse_lazy("backstage:actor-list")
    template_name = "backstage/actor_confirm_delete.html"


class DirectorListView(LoginRequiredMixin, generic.ListView):
    model = Director


class DirectorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Director
    queryset = Actor.objects.prefetch_related("awards").prefetch_related("plays")


class DirectorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Director
    fields = "__all__"
    success_url = reverse_lazy("backstage:director-list")


class DirectorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Director
    fields = "__all__"
    success_url = reverse_lazy("backstage:director-list")


class DirectorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Director
    success_url = reverse_lazy("backstage:director-list")
    template_name = "backstage/director_confirm_delete.html"


class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre


class GenreCreateView(LoginRequiredMixin, generic.CreateView):
    model = Genre
    fields = "__all__"
    success_url = reverse_lazy("backstage:genre-list")


class GenreUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Director
    fields = "__all__"
    success_url = reverse_lazy("backstage:genre-list")


class GenreDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Genre
    success_url = reverse_lazy("backstage:genre-list")
    template_name = "backstage/genre_confirm_delete.html"


class PlayListView(LoginRequiredMixin, generic.ListView):
    model = Play
    form_class = PlaySearchForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PlayListView, self).get_context_data(**kwargs)
        context["search"] = PlaySearchForm()

        name = self.request.GET.get("name", "")

        context["search"] = PlaySearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        today = date.today()

        queryset = Play.objects.prefetch_related("awards").prefetch_related("actors").prefetch_related("directors")
        form = PlaySearchForm(self.request.GET)

        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])

        play_list = queryset.filter(on_stage=True)
        archive_plays = queryset.filter(on_stage=False, day_of_premiere__lt=today)
        upcoming_plays = queryset.filter(on_stage=False, day_of_premiere__gt=today)

        return {
            'play-list': play_list,
            "archive_plays": archive_plays,
            'upcoming_plays': upcoming_plays
        }

    def get_template_names(self):
        if 'play-list' in self.object_list:
            return ['backstage/play-list.html']
        elif "archive_plays" in self.object_list:
            return ['backstage/play_archive.html']
        elif 'upcoming-plays' in self.object_list:
            return ['backstage/upcoming_play_list.html']
        else:
            return super().get_template_names()


class PlayDetailView(LoginRequiredMixin, generic.DetailView):
    model = Play
    queryset = Actor.objects.prefetch_related("awards").prefetch_related("plays")


class PlayCreateView(LoginRequiredMixin, generic.CreateView):
    model = Play
    form_class = PlayForm
    success_url = reverse_lazy("backstage:play-list")


class PlayUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Play
    form_class  = PlayForm
    success_url = reverse_lazy("backstage:play-list")


class PlayDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Play
    success_url = reverse_lazy("backstage:play-list")
    template_name = "backstage/play_confirm_delete.html"


class AwardListView(LoginRequiredMixin, generic.ListView):
    model = Award


class AwardCreateView(LoginRequiredMixin, generic.CreateView):
    model = Award
    fields = "__all__"
    success_url = reverse_lazy("backstage:plays-list")


class AwardUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Award
    fields = "__all__"
    success_url = reverse_lazy("backstage:award-list")


class AwardDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Award
    success_url = reverse_lazy("backstage:award-list")
    template_name = "backstage/award_confirm_delete.html"
