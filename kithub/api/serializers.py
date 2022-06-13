from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class KitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kit
        fields = "__all__"


class KitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitType
        fields = "__all__"
