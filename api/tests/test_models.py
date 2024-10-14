from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from api.tests.fixtures import user_fixture, theatre_hall_fixture, genre_fixture, actor_fixture, play_fixture, \
    performance_fixture


class TestTheatreModels(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

        self.theatre_hall = theatre_hall_fixture()
        self.genre = genre_fixture()
        self.actor = actor_fixture()
        self.play = play_fixture()
        self.performance = performance_fixture()


    def test_theatre_hall_capacity(self):
        self.assertEqual(self.theatre_hall.capacity, 100)

    def test_theatre_hall_str(self):
        self.assertEqual(
            str(self.theatre_hall),
            f"Hall {self.theatre_hall.name} has {self.theatre_hall.capacity} seats"
        )