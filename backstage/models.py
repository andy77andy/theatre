from django.db import models
from django.contrib.auth.models import AbstractUser

from theatre import settings


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Actor(AbstractUser):
    average_fee = models.PositiveIntegerField(default=1000)
    year_of_joining = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    class Meta:
        ordering = ["last_name"]
        verbose_name_plural = "actors"


class Director(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Play(models.Model):
    name = models.CharField(max_length=255, unique=True)
    troupe = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="plays")
    on_stage = models.BooleanField(default=True)
    day_of_premiere = models.DateField(blank=True, null=True)
    description = models.TextField(default="Best ever play")
    director = models.ForeignKey(Director, on_delete=models.DO_NOTHING, related_name="plays")
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING, related_name="plays", blank=True, null=True)

    class Meta:
        ordering = ["day_of_premiere"]

    def __str__(self):
        return f"{self.name}, {self.genre}, director: {self.director}"


class Review(models.Model):
    source = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    text = models.TextField(default="Best ever play")
    header = models.CharField(max_length=500, default="Best ever play")
    play = models.ForeignKey(Play, on_delete=models.DO_NOTHING, related_name="reviews", blank=True, null=True)
    author = models.CharField(max_length=200)

    def __str__(self):
        return {self.header}

    class Meta:
        ordering = ["-date"]


class Award(models.Model):
    name = models.CharField(max_length=50)
    nomination = models.CharField(max_length=50, null=True)
    year = models.PositiveIntegerField()
    actor = models.ForeignKey(Actor, on_delete=models.SET_NULL, related_name="awards", null=True)
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, related_name="director_awards", null=True)
    play = models.ForeignKey(Play, on_delete=models.SET_NULL, related_name="play_awards", null=True)
