from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234"
        )
        self.client.force_login(self.admin_user)
        self.actor = get_user_model().objects.create_user(
            username="user",
            password="admin1234",
            average_fee=1200
        )

    def test_actor_average_fee(self):
        url = reverse("admin:backstage_actor_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.actor.average_fee)

    def test_actor_detailed_average_fee(self):
        url = reverse("admin:backstage_actor_change", args=[self.actor.id])
        res = self.client.get(url)

        self.assertContains(res, self.actor.average_fee)
