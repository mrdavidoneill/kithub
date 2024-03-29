from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


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


class BagIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = BagIngredient
        fields = "__all__"


class BagTypeSerializer(serializers.ModelSerializer):
    ingredients = BagIngredientSerializer(many=True, read_only=True)

    class Meta:
        model = BagType
        fields = ["id", "kind", "ingredients"]


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"


class PartSerializer(serializers.ModelSerializer):
    purchases = PurchaseSerializer(many=True, read_only=True)

    class Meta:
        model = Part
        fields = ["id", "name", "description", "quantity", "purchases"]


class KitIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitIngredient
        fields = "__all__"
