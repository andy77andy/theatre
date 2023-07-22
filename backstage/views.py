import datetime
from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from backstage.forms import ActorCreationForm, ActorValidateUpdateDataForm, PlayForm, PlaySearchForm, ActorSearchForm, \
    AwardForm
from backstage.models import Award, Actor, Director, Play, Genre



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

    return render(request, "backstage/index2.html", context=context)


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
    queryset = Director.objects


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

        today = date.today()
        queryset = self.get_queryset()

        current_plays = queryset.filter(on_stage=True, day_of_premiere__lt=today)
        archive_plays = queryset.filter(on_stage=False, day_of_premiere__lt=today)
        upcoming_plays = queryset.filter(on_stage=False, day_of_premiere__gt=today)

        context.update({
            "current_plays": current_plays,
            "archive_plays": archive_plays,
            "upcoming_plays": upcoming_plays
        })

        return context

    def get_template_names(self) -> list[str]:
        if 'current' in self.request.path:
            return ['backstage/current_plays.html']
        elif "archive" in self.request.path:
            return ['backstage/play_archive.html']
        elif 'upcoming' in self.request.path:
            return ['backstage/upcoming_plays.html']
        else:
            return super().get_template_names()

    def get_queryset(self):
        queryset = Play.objects.all()
        form = PlaySearchForm(self.request.GET)

        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class PlayDetailView(LoginRequiredMixin, generic.DetailView):
    model = Play


class PlayCreateView(LoginRequiredMixin, generic.CreateView):
    model = Play
    form_class = PlayForm
    success_url = reverse_lazy("backstage:play-current")


class PlayUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Play
    form_class = PlayForm
    success_url = reverse_lazy("backstage:play-current")


class PlayDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Play
    success_url = reverse_lazy("backstage:play-current")
    template_name = "backstage/play_confirm_delete.html"


class AwardListView(LoginRequiredMixin, generic.ListView):
    model = Award

    @staticmethod
    def current_year():
        return datetime.date.today().year


class AwardCreateView(LoginRequiredMixin, generic.CreateView):
    model = Award
    form_class = AwardForm
    template_name = "backstage/award_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["actor_id"] = self.kwargs["pk"]
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        form = AwardForm(request.POST)
        pk = kwargs.get("pk")
        if form.is_valid():
            award = form.save(commit=False)
            award.actor_id = pk  # Assign the actor to the award
            award.save()
            return redirect('backstage:actor-detail', pk=pk)
            # if 'actors' in request.path:
            #     award.object_id = pk  # Assign the actor to the award
            #     award.save()
            #     return redirect('backstage:actor-detail', pk=pk)
            # if 'directors' in request.path:
            #     award.director(id=pk)  # Assign the actor to the award
            #     award.save()
            #     return redirect('backstage:director-detail', pk=pk)
            # if 'plays' in request.path:
            #     award.object_id = pk  # Assign the actor to the award
            #     award.save()
            #     return redirect('backstage:play-detail', pk=pk)
        else:
            return redirect('backstage:award_create', pk=pk)

    def get_success_url(self):
        return reverse_lazy('backstage:actor-detail', kwargs={"pk": self.kwargs.get("pk")})


class DirectorAwardCreateView(LoginRequiredMixin, generic.CreateView):
    model = Award
    form_class = AwardForm
    template_name = "backstage/award_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["director_id"] = self.kwargs["pk"]
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        form = AwardForm(request.POST)
        pk = kwargs.get("pk")
        if form.is_valid():
            award = form.save(commit=False)
            award.director_id = pk  # Assign the actor to the award
            award.save()
            return redirect('backstage:director-detail', pk=pk)
        else:
            return redirect('backstage:director_award_create', pk=pk)

    def get_success_url(self):
        return reverse_lazy('backstage:director-detail', kwargs={"pk": self.kwargs.get("pk")})


class PlayAwardCreateView(LoginRequiredMixin, generic.CreateView):
    model = Award
    form_class = AwardForm
    template_name = "backstage/award_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["play_id"] = self.kwargs["pk"]
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        form = AwardForm(request.POST)
        pk = kwargs.get("pk")
        if form.is_valid():
            award = form.save(commit=False)
            award.play_id = pk  # Assign the actor to the award
            award.save()
            return redirect('backstage:play-detail', pk=pk)
        else:
            return redirect('backstage:play_award_create', pk=pk)

    def get_success_url(self):
        return reverse_lazy('backstage:play-detail', kwargs={"pk": self.kwargs.get("pk")})


class AwardUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Award
    form_class = AwardForm
    success_url = reverse_lazy("backstage:award-list")


class AwardDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Award
    success_url = reverse_lazy("backstage:index")
    template_name = "backstage/award_confirm_delete.htm"


# @login_required
# def award_delete(request, pk):
#
#     award = Award.objects.get(id=pk)
#     actor_id = award.actor.id
#
#     if request.method == 'POST':
#         award.delete()
#         url = reverse('actor-detail', kwargs={'id': actor_id})
#         return HttpResponseRedirect(url)
#
#     # path('room/<str:pk>/', views.room_message, name='room')



