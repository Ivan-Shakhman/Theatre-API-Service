from rest_framework import serializers

from api.models import TheatreHall, Play, Actor, Genre


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("name", "rows", "seats_in_row", "capacity")


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("title", "description", "genres")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("first_name", "last_name")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name",)