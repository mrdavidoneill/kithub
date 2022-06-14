from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from kithub.api.serializers import UserSerializer, GroupSerializer
from .serializers import *


class KitViewSet(viewsets.ModelViewSet):
    queryset = Kit.objects.all()
    serializer_class = KitSerializer


class KitTypeViewSet(viewsets.ModelViewSet):
    queryset = KitType.objects.all()
    serializer_class = KitTypeSerializer


class BagViewSet(viewsets.ModelViewSet):
    queryset = Bag.objects.all()
    serializer_class = BagSerializer


class BagTypeViewSet(viewsets.ModelViewSet):
    queryset = BagType.objects.all()
    serializer_class = BagTypeSerializer


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class BagIngredientViewSet(viewsets.ModelViewSet):
    queryset = BagIngredient.objects.all()
    serializer_class = BagIngredientSerializer


class KitIngredientViewSet(viewsets.ModelViewSet):
    queryset = KitIngredient.objects.all()
    serializer_class = KitIngredientSerializer
