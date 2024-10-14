from datetime import datetime

from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.models import Genre, Actor, TheatreHall, Play, Performance, Reservation
from api.paginations import PlayPagination, ActorPagination, PerformancePagination, ReservationPagination
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
    pagination_class = ActorPagination


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
    pagination_class = PlayPagination

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        if self.action == "retrieve":
            return PlayDetailSerializer
        return PlaySerializer

    @staticmethod
    def _str_query_param_to_int(param):
        return [int(obj_id) for obj_id in param.split(",")]

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("genres", "actors")
        title = self.request.query_params.get("title", None)
        genres = self.request.query_params.get("genres", None)
        actors = self.request.query_params.get("actors", None)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if genres:
            genres_ids = self._str_query_param_to_int(genres)
            queryset = queryset.filter(genres__id__in=genres_ids)

        if actors:
            actors_ids = self._str_query_param_to_int(actors)
            queryset = queryset.filter(actors__id__in=actors_ids)
        return queryset

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific movie"""
        movie = self.get_object()
        serializer = self.get_serializer(movie, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PerformanceViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Performance.objects.select_related("theatre_hall", "play")
    serializer_class = PerformanceSerializer
    pagination_class = PerformancePagination

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
    pagination_class = ReservationPagination

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        return ReservationSerializer

    def get_queryset(self):
        query_set = self.queryset.filter(user=self.request.user)
        return query_set

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)