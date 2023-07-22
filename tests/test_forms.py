from django.test import TestCase

from backstage.forms import (
    ActorCreationForm, ActorValidateUpdateDataForm
)
from backstage.models import Actor


class FormsTests(TestCase):
    def test_actor_creation_added_fields(self):
        actor = {
            "username": "new_yorker",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Woody",
            "last_name": "Allen",
            "average_fee": 1100,
            "year_of_joining": 2000,
        }
        form = ActorCreationForm(data=actor)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, actor)

    def test_create_actor_invalid_fee(self):
        actor = {
            "username": "new_yorker",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Woody",
            "last_name": "Allen",
            "average_fee": 1100,
            "year_of_joining": 1999,
        }
        form = ActorCreationForm(data=actor)
        self.assertFalse(form.is_valid())

    def test_update_actor_invalid_fee(self):
        data = {
            "username": "new_yorker",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Woody",
            "last_name": "Allen",
            "average_fee": 1100,
            "year_of_joining": 2010,
        }
        form = ActorCreationForm(data=data)
        if form.is_valid():
            actor = form.save()
            updated_data = {
                "username": "new_yorker",
                "password1": "test12345",
                "password2": "test12345",
                "first_name": "Woody",
                "last_name": "Allen",
                "average_fee": 900,
                "year_of_joining": 1800,
            }

            form_2 = ActorValidateUpdateDataForm(data=updated_data, instance=actor)
            self.assertFalse(form_2.is_valid())
