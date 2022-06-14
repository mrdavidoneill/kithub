from rest_framework.decorators import api_view
from rest_framework.response import Response
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


def potential_kits_of_kittype(kittype):
    # Store number of potential kits according to each bag
    potential_bags = {}
    # Store lowest number of potential kits
    lowest_bag_num = None
    # Get all bagtypes that are needed for kittype
    bagtypes_needed = BagType.objects.filter(needed__kittype=kittype)
    # Iterate through each needed bag
    for bagtype in bagtypes_needed:
        # Get all bags currently in stock
        in_stock = Bag.objects.filter(kind=bagtype, complete=False)

        # Gather all and count quantities
        in_stock_quantity = 0
        for bag in in_stock:
            in_stock_quantity += bag.quantity

        # Calculate how many kits are possible with bags in stock
        potential_bags[bagtype.kind] = (
            in_stock_quantity
            // KitIngredient.objects.filter(kittype=kittype, bagtype=bagtype)
            .first()
            .quantity
        )

        # Store lowest num of bags in stock
        if lowest_bag_num is None or potential_bags[bagtype.kind] < lowest_bag_num:
            lowest_bag_num = potential_bags[bagtype.kind]

    return {
        "kittypeID": kittype,
        "potential_kits": lowest_bag_num,
        "potential_kits_by_bag": potential_bags,
    }


@api_view(["GET"])
def all_potentialkits(request):
    response = []
    kittypes = KitType.objects.all()
    for kittype in kittypes:
        response.append(potential_kits_of_kittype(kittype.pk))

    return Response(response)


@api_view(["GET"])
def potentialkits(request, kittype):
    return Response([potential_kits_of_kittype(kittype)])


def potential_bags_of_bagtype(bagtype):
    # Store number of potential bags according to each needed part
    parts_potential = {}
    # Store lowest number of potential bags
    lowest_part_num = None
    # Get all parts that are needed for bagtype
    parts_needed = Part.objects.filter(needed__bagtype=bagtype)
    # Iterate through each needed part
    for part in parts_needed:
        # Calculate how many bags are possible with parts in stock
        parts_potential[part.name] = (
            part.quantity
            // BagIngredient.objects.filter(bagtype=bagtype, part=part).first().quantity
        )

        # Store lowest num of parts in stock
        if lowest_part_num is None or parts_potential[part.name] < lowest_part_num:
            lowest_part_num = parts_potential[part.name]

    return {
        "bagtypeID": bagtype,
        "potential_bags": lowest_part_num,
        "potential_bags_by_part": parts_potential,
    }


@api_view(["GET"])
def all_potentialbags(request):
    response = []
    bagtypes = BagType.objects.all()
    for bagtype in bagtypes:
        response.append(potential_bags_of_bagtype(bagtype.pk))

    return Response(response)


@api_view(["GET"])
def potentialbags(request, bagtype):
    return Response([potential_bags_of_bagtype(bagtype)])
