from django.contrib.auth import get_user_model
from django.urls import reverse

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Genre, Actor, TheatreHall, Play
from api.tests.fixtures import genre_fixture, actor_fixture, theatre_hall_fixture, play_fixture

PLAY_URL = reverse("api:play-list")

class GenreViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)
        self.genre = genre_fixture()
        self.list_url = reverse("api:genre-list")
        self.create_url = reverse("api:genre-list")

    def test_list_genres(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_genre(self):
        data = {"name": "Comedy"}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Genre.objects.count(), 1)


class ActorViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)
        self.actor = actor_fixture()
        self.list_url = reverse("api:actor-list")
        self.create_url = reverse("api:actor-list")

    def test_list_actors(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_actor(self):
        data = {"first_name": "Jane", "last_name": "Doe"}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Actor.objects.count(), 2)


class TheatreHallViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)
        self.theatre_hall = theatre_hall_fixture()
        self.list_url = reverse("api:theatrehall-list")
        self.create_url = reverse("api:theatrehall-list")

    def test_list_theatre_halls(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_theatre_hall(self):
        data = {"name": "Small Hall", "rows": 5, "seats_in_row": 15}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TheatreHall.objects.count(), 2)


class PlayViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)
        self.genre = genre_fixture()
        self.actor = actor_fixture()
        self.play = play_fixture()

        self.list_url = reverse("api:play-list")
        self.detail_url = reverse("api:play-detail", args=[self.play.id])

    def test_list_plays(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_play(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test play title")

    def test_create_play(self):
        data = {
            "title": "Macbeth",
            "description": "Another Shakespeare play",
            "genres": [self.genre.id],
            "actors": [self.actor.id]
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Play.objects.count(), 2)


