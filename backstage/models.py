from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from theatre import settings


class Award(models.Model):
    name = models.CharField(max_length=255)
    nomination = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.nomination}, {self.year})"


class Actor(AbstractUser):
    average_fee = models.CharField(max_length=255)
    award = models.ManyToManyField(Award, related_name="actor_awards")

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    # def get_absolute_url(self):
    #     return reverse("taxi:driver-detail", kwargs={"pk": self.pk})


class Director(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    award = models.ManyToManyField(Award, related_name="director_awards")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Play(models.Model):
    name = models.CharField(max_length=255, unique=True)
    troupe = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="actors")
    on_stage = models.BooleanField()
    day_of_premiere = models.DateTimeField(auto_now=True)
    director = models.ForeignKey(Director, on_delete=models.DO_NOTHING)
    award = models.ManyToManyField(Award, related_name="awards")

    class Meta:
        ordering = ["day_of_premiere"]

    def __str__(self):
        if self.award:
            return f"{self.name}, director, {self.director}, awarded by {self.award}"
        return f"{self.name}, director, {self.director}"


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
