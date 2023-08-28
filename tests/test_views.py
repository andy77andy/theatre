from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from backstage.models import Genre, Award, Play, Director

GENRE_LIST_URL = reverse("backstage:genre-list")
DIRECTOR_LIST_URL = reverse("backstage:director-list")
AWARD_LIST_URL = reverse("backstage:award-list")
PLAY_LIST_URL = reverse("backstage:play-list")
ACTOR_LIST_URL = reverse("backstage:actor-list")
ACTOR_REDIRECT_PUBLIC_URL = reverse("login")


class PrivateGenreListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="Test123456",
        )
        self.client.force_login(self.user)

    def test_retrieve_genres(self):
        Genre.objects.create(name="dramedy")
        response = self.client.get(GENRE_LIST_URL)
        genres = Genre.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["genre_list"]),
                         list(genres))


class PrivateAwardListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="Test123456",
        )
        self.client.force_login(self.user)


    def test_retrieve_awards(self):
        Award.objects.create(name="Test", nomination="test", year=2000)
        response = self.client.get(AWARD_LIST_URL)
        awards = Award.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["award_list"]),
                         list(awards))

    # def test_manufacturer_search(self):
    #     Manufacturer.objects.create(name="Lincoln", country="USA")
    #     response = self.client.get(MANUFACTURER_LIST_URL, {"name": "Lincoln"})
    #     search_manufacturer = Manufacturer.objects.filter(name="Lincoln")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(list(response.context["manufacturer_list"]),
    #                      list(search_manufacturer))

#
class PublicDirectorListTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DIRECTOR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

class PublicPlayListTests(TestCase):
    def test_login_required(self):
        response = self.client.get(PLAY_LIST_URL)
        self.assertNotEqual(response, 200)


class PrivatePlayListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="Test123456",
        )
        self.client.force_login(self.user)

    def test_retrieve_plays(self):
        test_director = Director.objects.create(
            first_name="test", last_name="Test")
        test_genre = Genre.objects.create(name="test",)

        test_play = Play.objects.create(
            name="test",
            director=test_director,
            genre=test_genre,
        )
        response = self.client.get(PLAY_LIST_URL)
        plays = Play.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["play_list"]),
                         list(plays))

    def test_play_search(self):
        test_director = Director.objects.create(
            first_name="test", last_name="Test")
        test_genre = Genre.objects.create(name="test", )

        test_play = Play.objects.create(
           name="test",
           director=test_director,
           genre=test_genre,
        )
        response = self.client.get(PLAY_LIST_URL, {"name": "test"})
        search_play = Play.objects.filter(name="test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["play_list"]),
                         list(search_play))


class PublicActorListTests(TestCase):
    def test_login_required(self):
        response = self.client.get(ACTOR_LIST_URL)
        self.assertTemplateUsed("registration/login.html")


class PrivateActorTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Andy",
            password="Andy123456",
        )
        self.client.force_login(self.user)

    def test_retrieve_actors(self):
        form_actor = {
            "username": "new_yorker",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Woody",
            "last_name": "Allen",
            "average_fee": 1100,
            "year_of_joining": 2000,
        }
        self.client.post(reverse("backstage:actor-create"), data=form_actor)
        response = self.client.get(ACTOR_LIST_URL)
        new_user = get_user_model().objects.get(
            username=form_actor["username"]
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_user.last_name, "Allen")
        self.assertEqual(new_user.first_name, form_actor["first_name"])
        self.assertTemplateUsed(response, "backstage/actor_list.html")

    def test_actor_search(self):
        form_actor = {
            "username": "new_yorker",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Woody",
            "last_name": "Allen",
            "average_fee": 1100,
            "year_of_joining": 2000,
        }
        self.client.post(reverse("backstage:actor-create"), data=form_actor)
        response = self.client.get(
            ACTOR_LIST_URL, {"last_name": "Allen"}
        )
        actor_search = get_user_model().objects.filter(last_name="Allen")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["actor_list"]),
                         list(actor_search))
