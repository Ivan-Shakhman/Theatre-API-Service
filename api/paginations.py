from rest_framework.pagination import PageNumberPagination


class PlayPagination(PageNumberPagination):
    page_size = 12
    max_page_size = 60


class ReservationPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 25


class ActorPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100


class PerformancePagination(PageNumberPagination):
    page_size = 8
    max_page_size = 40