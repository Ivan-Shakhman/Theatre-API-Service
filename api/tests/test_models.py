from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError as ValidationErrorCore
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from api.models import Ticket, TheatreHall, Performance, Reservation
from api.tests.fixtures import user_fixture, theatre_hall_fixture, genre_fixture, actor_fixture, play_fixture, \
    performance_fixture


class TestTheatreModels(TestCase):

    def setUp(self):
        self.theatre_hall = theatre_hall_fixture()


    def test_theatre_hall_capacity(self):
        self.assertEqual(self.theatre_hall.capacity, 100)

    def test_theatre_hall_str(self):
        self.assertEqual(
            str(self.theatre_hall),
            f"Hall {self.theatre_hall.name} "
            f"has {self.theatre_hall.capacity} seats"
        )


class TestGenreModels(TestCase):
    def setUp(self):
        self.genre = genre_fixture()

    def test_genre_str(self):
        self.assertEqual(str(self.genre), "Test genre")


class TestActorModels(TestCase):
    def setUp(self):
        self.actor = actor_fixture()

    def test_actor_str_and_fullname_property(self):
        self.assertEqual(self.actor.full_name, "John Doe")
        self.assertEqual(self.actor.full_name, str(self.actor))


class ReservationModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='password123'
        )
        self.theatre_hall = theatre_hall_fixture()
        self.performance = performance_fixture(theatre_hall=self.theatre_hall)

    def test_create_reservation(self):
        reservation = Reservation.objects.create(user=self.user)
        self.assertIsInstance(reservation, Reservation)
        self.assertEqual(reservation.user, self.user)


class TicketModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='password123'
        )
        self.theatre_hall = theatre_hall_fixture()
        self.performance = performance_fixture(theatre_hall=self.theatre_hall)
        self.reservation = Reservation.objects.create(user=self.user)

    def test_create_ticket(self):
        ticket = Ticket.objects.create(
            row=1,
            seat=1,
            performance=self.performance,
            reservation=self.reservation
        )
        self.assertIsInstance(ticket, Ticket)
        self.assertEqual(ticket.row, 1)
        self.assertEqual(ticket.seat, 1)
        self.assertEqual(ticket.performance, self.performance)
        self.assertEqual(ticket.reservation, self.reservation)

    def test_ticket_validation_success(self):
        ticket = Ticket(
            row=1,
            seat=1,
            performance=self.performance,
            reservation=self.reservation
        )
        ticket.clean()
        ticket.save()

    def test_ticket_validation_failure_row(self):
        ticket = Ticket(
            row=11,
            seat=1,
            performance=self.performance,
            reservation=self.reservation
        )
        with self.assertRaises(ValidationError):
            ticket.clean()

    def test_ticket_validation_failure_seat(self):
        ticket = Ticket(
            row=1,
            seat=11,
            performance=self.performance,
            reservation=self.reservation
        )
        with self.assertRaises(ValidationError):
            ticket.clean()

    def test_unique_ticket_constraint(self):
        Ticket.objects.create(
            row=1,
            seat=1,
            performance=self.performance,
            reservation=self.reservation
        )
        with self.assertRaises(ValidationErrorCore):
            Ticket.objects.create(
                row=1,
                seat=1,
                performance=self.performance,
                reservation=self.reservation
            )