from rest_framework import serializers

from api.models import TheatreHall, Play, Actor, Genre, Performance


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