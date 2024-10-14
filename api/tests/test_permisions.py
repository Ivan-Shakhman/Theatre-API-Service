from rest_framework.permissions import IsAdminUser
from rest_framework.test import APIRequestFactory, force_authenticate
from user.models import User
from django.test import TestCase
from api.permissions import IsAdminOrIfAuthenticatedReadOnly


class IsAdminOrIfAuthenticatedReadOnlyTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.permission = IsAdminOrIfAuthenticatedReadOnly()
        self.admin_user = User.objects.create_user(
            email="admin@admin.com", password="admin", is_staff=True
        )
        self.regular_user = User.objects.create_user(
            email="user@user.com", password="user"
        )
        self.anonymous_user = None

    def test_anonymous_user_not_read_access(self):
        request = self.factory.get("/some-url/")
        request.user = self.anonymous_user
        self.assertFalse(self.permission.has_permission(request, None))

    def test_anonymous_user_write_access(self):
        request = self.factory.post("/some-url/")
        request.user = self.anonymous_user
        self.assertFalse(self.permission.has_permission(request, None))

    def test_authenticated_user_read_access(self):
        request = self.factory.get("/some-url/")
        request.user = self.regular_user
        self.assertTrue(self.permission.has_permission(request, None))

    def test_authenticated_user_write_access(self):
        request = self.factory.post("/some-url/")
        request.user = self.regular_user
        self.assertFalse(self.permission.has_permission(request, None))

    def test_admin_user_read_access(self):
        request = self.factory.get("/some-url/")
        request.user = self.admin_user
        self.assertTrue(self.permission.has_permission(request, None))

    def test_admin_user_write_access(self):
        request = self.factory.post("/some-url/")
        request.user = self.admin_user
        self.assertTrue(self.permission.has_permission(request, None))
