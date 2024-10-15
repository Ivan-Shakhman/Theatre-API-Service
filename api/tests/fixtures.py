from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from api.models import TheatreHall, Genre, Actor, Play, Performance, Reservation


def user_fixture(**kwargs):
    client = APIClient()
    user_data = {
        "email": "testuser@test.com",
        "password": "testpass",
    }
    user_data.update(kwargs)
    user = get_user_model().objects.create_user(**user_data)
    client.force_authenticate(user)


def theatre_hall_fixture(**kwargs):
    hall_set_up = {"name": "Test theatre hall", "rows": 10, "seats_in_row": 10}
    hall_set_up.update(kwargs)
    return TheatreHall.objects.create(**hall_set_up)


def genre_fixture(**kwargs):
    genre_set_up = {
        "name": "Test genre",
    }
    genre_set_up.update(kwargs)
    return Genre.objects.create(**genre_set_up)


def actor_fixture(**kwargs):
    actor_set_up = {
        "first_name": "John",
        "last_name": "Doe",
    }
    actor_set_up.update(kwargs)
    return Actor.objects.create(**actor_set_up)


def play_fixture(**kwargs):
    genres = genre_fixture(name="another genre"), genre_fixture()
    actors = (
        actor_fixture(
            first_name="another first name",
            last_name="another last name",
        ),
        actor_fixture(),
    )
    play_set_up = {
        "title": "Test play title",
        "description": "Test play description",
        "image": None,
    }
    play_set_up.update(kwargs)

    default = Play.objects.create(**play_set_up)
    default.genres.set(genres)
    default.actors.set(actors)

    return default


def performance_fixture(**kwargs):
    performance_set_up = {
        "play": play_fixture(),
        "theatre_hall": theatre_hall_fixture(),
        "show_time": "2023-10-14 20:00",
    }
    performance_set_up.update(kwargs)
    return Performance.objects.create(**performance_set_up)
