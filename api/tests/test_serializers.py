from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.test import APITestCase, APIClient
from api.models import TheatreHall, Play, Actor, Genre, Performance, Ticket, Reservation
from api.serializers import (
    TheatreHallSerializer,
    ActorSerializer,
    GenreSerializer,
    PlaySerializer,
    PerformanceSerializer,
    TicketSerializer,
    ReservationSerializer
)
from api.tests.fixtures import theatre_hall_fixture, genre_fixture, actor_fixture, play_fixture, performance_fixture


class TheatreHallSerializerTest(APITestCase):
    def setUp(self):
        self.theatre_hall = theatre_hall_fixture()

    def test_theatre_hall_serialization(self):
        serializer = TheatreHallSerializer(self.theatre_hall)
        self.assertEqual(serializer.data, {
        "name": "Test theatre hall",
        "rows": 10,
        "seats_in_row": 10,
        "capacity": 100,
    })


class ActorSerializerTest(APITestCase):
    def setUp(self):
        self.actor = Actor.objects.create(first_name="John", last_name="Doe")

    def test_actor_serialization(self):
        serializer = ActorSerializer(self.actor)
        self.assertEqual(serializer.data, {
            "first_name": "John",
            "last_name": "Doe"
        })


class GenreSerializerTest(APITestCase):
    def setUp(self):
        self.genre = genre_fixture()

    def test_genre_serialization(self):
        serializer = GenreSerializer(self.genre)
        self.assertEqual(serializer.data, {
            "name": "Test genre"
        })


class PlaySerializerTest(APITestCase):
    def setUp(self):
        self.play = play_fixture()


    def test_play_serialization(self):
        serializer = PlaySerializer(self.play)
        self.assertEqual(serializer.data, {
            "title": "Test play title",
            "description": "Test play description",
            "image": None,
            "genres": [2, 1],
            "actors": [2, 1],
        })


class PerformanceSerializerTest(APITestCase):
    def setUp(self):
        self.performance = performance_fixture()

    def test_performance_serialization(self):
        serializer = PerformanceSerializer(self.performance)
        self.assertEqual(serializer.data, {
        "play": self.performance.play.pk,
        "theatre_hall": self.performance.theatre_hall.pk,
        "show_time": "2023-10-14 20:00"
    })


class TicketSerializerTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)
        self.performance = performance_fixture()
        self.reservation = Reservation.objects.create(user=self.user)

    def test_ticket_creation(self):
        data = {
            "row": 1,
            "seat": 1,
            "performance": self.performance.pk
        }
        serializer = TicketSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        ticket = serializer.save(reservation=self.reservation)
        self.assertEqual(ticket.row, 1)
        self.assertEqual(ticket.seat, 1)
        self.assertEqual(ticket.performance, self.performance)

    def test_duplicate_ticket_validation(self):
        Ticket.objects.create(row=1, seat=1, performance=self.performance, reservation=self.reservation)
        data = {
            'row': 1,
            'seat': 1,
            'performance': self.performance.pk
        }
        serializer = TicketSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

class ReservationSerializerTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)
        self.performance = performance_fixture()
        self.reservation_data = {
            "tickets": [
                {"row": 1, 'seat': 1, 'performance': self.performance.pk},
                {'row': 1, 'seat': 2, 'performance': self.performance.pk}
            ],
        }

    def test_reservation_creation(self):
        serializer = ReservationSerializer(data=self.reservation_data)
        self.assertTrue(serializer.is_valid())
        reservation = serializer.save(user=self.user)
        self.assertEqual(reservation.tickets.count(), 2)

    def test_reservation_with_duplicate_tickets(self):
        Ticket.objects.create(
            row=1,
            seat=1,
            performance=self.performance,
            reservation=Reservation.objects.create(user=self.user)
        )
        serializer = ReservationSerializer(data=self.reservation_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('tickets', serializer.errors)