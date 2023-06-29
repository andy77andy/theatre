from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.urls import reverse
#
# from backstage.forms import max_value_current_year
from theatre import settings


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Award(models.Model):
    name = models.CharField(max_length=255)
    nomination = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.nomination}, {self.year})"

    class Meta:
        ordering = ["name"]


class Actor(AbstractUser):
    average_fee = models.CharField(max_length=255)
    awards = models.ManyToManyField(Award, related_name="actor_awards", null=True, blank=True)
    year_of_joining = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    class Meta:
        ordering = ["last_name"]
        verbose_name_plural = "actors"


class Director(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    awards = models.ManyToManyField(Award, related_name="director_awards", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Play(models.Model):
    name = models.CharField(max_length=255, unique=True)
    troupe = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="plays")
    on_stage = models.BooleanField()
    day_of_premiere = models.DateField(blank=True, null=True)
    description = models.TextField(default="Best ever play")
    director = models.ForeignKey(Director, on_delete=models.DO_NOTHING, related_name="plays")
    awards = models.ManyToManyField(Award, related_name="awards", blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING, related_name="plays", blank=True, null=True)

    class Meta:
        ordering = ["day_of_premiere"]

    def __str__(self):
        if self.awards:
            return f"{self.name}, director, {self.director}, awarded by {self.awards}"
        return f"{self.name}, {self.genre}, director: {self.director}"
