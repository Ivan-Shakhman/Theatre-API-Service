from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserManagerTest(TestCase):

    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "password123"
        self.user_manager = User.objects

    def test_create_user(self):
        user = self.user_manager.create_user(email=self.email, password=self.password)

        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = self.user_manager.create_superuser(email=self.email, password=self.password)

        self.assertEqual(superuser.email, self.email)
        self.assertTrue(superuser.check_password(self.password))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError) as cm:
            self.user_manager.create_user(email="", password=self.password)
        self.assertEqual(str(cm.exception), "The given email must be set")

    def test_create_superuser_without_staff_flag(self):
        with self.assertRaises(ValueError) as cm:
            self.user_manager.create_superuser(email=self.email, password=self.password, is_staff=False)
        self.assertEqual(str(cm.exception), "Superuser must have is_staff=True.")

    def test_create_superuser_without_superuser_flag(self):
        with self.assertRaises(ValueError) as cm:
            self.user_manager.create_superuser(email=self.email, password=self.password, is_superuser=False)
        self.assertEqual(str(cm.exception), "Superuser must have is_superuser=True.")


class UserTest(TestCase):

    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "password123"
        self.user = User.objects.create_user(email=self.email, password=self.password)

    def test_user_creation(self):
        self.assertEqual(self.user.email, self.email)
        self.assertTrue(self.user.check_password(self.password))
        self.assertIsNone(self.user.username)

    def test_user_str(self):
        self.assertEqual(str(self.user), self.user.email)

    def test_user_repr(self):
        self.assertEqual(repr(self.user), f"<User: {self.user.email}>")
