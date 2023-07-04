from django.contrib.auth import get_user_model
from django.test import TestCase

from backstage.models import Director, Genre, Play


class ModelsTESTS(TestCase):
    def test_director_str(self):
        test_director = Director.objects.create(
            first_name="test", last_name="Test")
        self.assertEqual(str(
            test_director),
            f"{test_director.first_name} "
            f"{test_director.last_name}")

    def test_actor_str(self):
        test_actor = get_user_model().objects.create_user(username="test",
                                                          password="test1234",
                                                          first_name="test",
                                                          last_name="test",
                                                          )

        self.assertEqual(str(test_actor),
                         f"{test_actor.username} "
                         f"({test_actor.first_name} "
                         f"{test_actor.last_name})")

    def test_create_actor_with_average_fee_and_year_of_joining(self):
        test_actor = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="test",
            last_name="test",
            average_fee=100,
            year_of_joining=1992,
        )

        self.assertTrue(test_actor)
        self.assertTrue(test_actor.check_password("test1234"))

    def test_genre_str(self):
        # test_genre = Genre.objects.create(name="test",)
        test_genre = Genre.objects.create(name="test", )

        self.assertEqual(str(test_genre), f"{test_genre.name}")

    def test_play_str(self):
        test_director = Director.objects.create(
            first_name="test", last_name="Test")
        test_genre = Genre.objects.create(name="test", )

        test_play = Play.objects.create(
            name="test",
            director=test_director,
            genre=test_genre,
        )

        self.assertEqual(str(test_play), f"{test_play.name}, {test_play.genre}, director: {test_play.director}")
