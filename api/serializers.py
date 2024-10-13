from django.db import transaction
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import TheatreHall, Play, Actor, Genre, Performance, Ticket, Reservation


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("name", "rows", "seats_in_row", "capacity")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("first_name", "last_name")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name",)


class PlaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = ("title", "description", "genres", "actors")


class PlayListSerializer(PlaySerializer):
    genres = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    actors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )

    class Meta:
        model = Play
        fields = ("title", "description", "genres", "actors")


class PlayDetailSerializer(PlaySerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = ("title", "description", "genres", "actors")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("play", "theatre_hall", "show_time")


class PerformanceListSerializer(PerformanceSerializer):
    theatre_hall = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )
    play = serializers.SlugRelatedField(
        read_only=True, slug_field="title"
    )

    class Meta:
        model = Performance
        fields = ("play", "theatre_hall", "show_time")


class PerformanceDetailSerializer(PerformanceSerializer):
    theatre_hall = TheatreHallSerializer(read_only=True)
    play = PlaySerializer(read_only=True)

    class Meta:
        model = Performance
        fields = ("theatre_hall", "play", "show_time")

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat", "performance")

    def validate(self, data):
        performance = data["performance"]
        if Ticket.objects.filter(
                row=data["row"],
                seat=data["seat"],
                performance=performance
        ).exists():
            raise serializers.ValidationError(
                f"Ticket with row-{data['row']}, seat-{data['seat']} "
                f"already exists for performance {performance}."
            )

        theatre_hall = performance.theatre_hall
        Ticket.validate_ticket(
            data["row"],
            data["seat"],
            theatre_hall,
            serializers.ValidationError
        )
        return data


class TicketListSerializer(TicketSerializer):

    class Meta:
        model = Ticket
        fields = ("row", "seat", "performance")


class TicketDetailSerializer(TicketSerializer):
    performance = PerformanceSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ("row", "seat", "performance")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, )

    class Meta:
        model = Reservation
        fields = ("created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)

            for ticket_data in tickets_data:

                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    class Meta:
        model = Reservation
        fields = ("id", "created_at", "tickets")