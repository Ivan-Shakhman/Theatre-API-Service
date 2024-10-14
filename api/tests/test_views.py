from django.urls import reverse

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


PLAY_URL = reverse("api:play-list")




class UnauthenticatedPlayApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLAY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# class AuthenticatedPlayApiTests(TestCase):
#