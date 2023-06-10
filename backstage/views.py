from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from backstage.models import Award, Actor, Director, Play


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
