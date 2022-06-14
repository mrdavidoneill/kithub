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
    name = serializers.CharField(
        trim_whitespace=False, max_length=255, allow_blank=True
    )

    class Meta:
        model = Kit
        fields = "__all__"


class KitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitType
        fields = "__all__"


class BagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        trim_whitespace=False, max_length=255, allow_blank=True
    )

    class Meta:
        model = Bag
        fields = "__all__"


class BagTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BagType
        fields = "__all__"


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"
