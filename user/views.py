from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from api import permissions
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
	serializer_class = UserSerializer
	permission_classes = (AllowAny,)

class ManageUserView(generics.RetrieveUpdateAPIView):
	serializer_class = UserSerializer


	def get_object(self):
		return self.request.user
