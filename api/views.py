from datetime import datetime

from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.models import Genre, Actor, TheatreHall, Play, Performance, Reservation
from api.serializers import GenreSerializer, ActorSerializer, TheatreHallSerializer, PlaySerializer, PlayListSerializer, \
    PlayDetailSerializer, PerformanceSerializer, PerformanceListSerializer, PerformanceDetailSerializer, \
    ReservationSerializer, ReservationListSerializer


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class TheatreHallViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PlayViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Play.objects.prefetch_related("genres", "actors")
    serializer_class = PlaySerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        if self.action == "retrieve":
            return PlayDetailSerializer
        return PlaySerializer


class PerformanceViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Performance.objects.select_related("theatre_hall", "play")
    serializer_class = PerformanceSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        return PerformanceSerializer

    def get_queryset(self):
        query_set = self.queryset
        date = self.request.query_params.get("date")
        play_id = self.request.query_params.get("play")
        if date:
            date = datetime.strptime(date, "%d-%m-%Y").date()
            query_set = query_set.filter(show_time__date=date)
        if play_id:
            query_set = query_set.filter(play_id=play_id)
        return query_set.distinct()


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        return ReservationSerializer

    def get_queryset(self):
        query_set = self.queryset.filter(user=self.request.user)
        return query_set

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)