from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from kithub.api.serializers import UserSerializer, GroupSerializer
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class KitViewSet(viewsets.ModelViewSet):
    queryset = Kit.objects.all()
    serializer_class = KitSerializer


class KitTypeViewSet(viewsets.ModelViewSet):
    queryset = KitType.objects.all()
    serializer_class = KitTypeSerializer
