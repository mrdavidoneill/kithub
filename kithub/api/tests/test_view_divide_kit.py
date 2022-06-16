import json
from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import status

from ..models import *
from ..serializers import *
from . import common


class GetAllPotentialKits(TestCase):
    """Test module for retrieving all potential kits"""

    def setUp(self):

        self.route = "dividekit"
        self.client = APIClient()

        # Create stock

        # Create 10 parts with 10 quantity of each
        self.parts = []
        for i in range(10):
            self.parts.append(
                Part.objects.create(
                    name=f"part{i}",
                    description=f"description for part{i}",
                    quantity=10,
                )
            )
        # Create 3 bagtypes
        self.bagtypes = []
        for i in range(3):
            self.bagtypes.append(BagType.objects.create(kind=f"bagtype{i}"))

        # Create 3 kittypes
        self.kittypes = []
        for i in range(3):
            self.kittypes.append(KitType.objects.create(kind=f"kittype{i}"))

        # Create bagingredients for bagtype0
        # 1 of each part
        self.bagingredients = []
        for i, part in enumerate(self.parts):
            self.bagingredients.append(
                BagIngredient.objects.create(
                    name=string.ascii_letters[i].upper(),
                    bagtype=self.bagtypes[0],
                    part=part,
                    quantity=1,
                )
            )

        # Create bagingredients for bagtype1
        # 2 of each part
        self.bagingredients = []
        for i, part in enumerate(self.parts):
            self.bagingredients.append(
                BagIngredient.objects.create(
                    name=string.ascii_letters[i].upper(),
                    bagtype=self.bagtypes[1],
                    part=part,
                    quantity=2,
                )
            )

        # Create bagingredients for bagtype2
        # 1 of first two parts
        self.bagingredients = []
        for i, part in enumerate(self.parts[:2]):
            self.bagingredients.append(
                BagIngredient.objects.create(
                    name=string.ascii_letters[i].upper(),
                    bagtype=self.bagtypes[2],
                    part=part,
                    quantity=1,
                )
            )

        self.kitingredients = []

        # Create kitingredients for kittype0
        # 1 of each bagtype
        self.kitingredients = []
        for i, bagtype in enumerate(self.bagtypes):
            self.kitingredients.append(
                KitIngredient.objects.create(
                    name=string.ascii_letters[i].upper(),
                    kittype=self.kittypes[0],
                    bagtype=bagtype,
                    quantity=1,
                )
            )

        # Create kitingredients for kittype1
        # 2 of each bagtype
        self.kitingredients = []
        for i, bagtype in enumerate(self.bagtypes):
            self.kitingredients.append(
                KitIngredient.objects.create(
                    name=string.ascii_letters[i].upper(),
                    kittype=self.kittypes[1],
                    bagtype=bagtype,
                    quantity=2,
                )
            )

        # Create kitingredients for kittype2
        # 1 of first two parts
        self.kitingredients = []
        for i, bagtype in enumerate(self.bagtypes[:2]):
            self.kitingredients.append(
                KitIngredient.objects.create(
                    name=string.ascii_letters[i].upper(),
                    kittype=self.kittypes[2],
                    bagtype=bagtype,
                    quantity=1,
                )
            )

        # Create 10 complete bags of each bagtype
        self.bags = []
        for i, bagtype in enumerate(self.bagtypes):
            # Get complete name
            parts_needed = Part.objects.filter(needed__bagtype=bagtype)
            name = string.ascii_letters[: len(parts_needed)].upper()
            self.bags.append(
                Bag.objects.create(
                    name=name,
                    quantity=10,
                    complete=True,
                    kind=bagtype,
                )
            )

        # Create 10 complete kits of each kittype
        self.kits = []
        for i, kittype in enumerate(self.kittypes):
            # Get complete name
            bagtypes_needed = BagType.objects.filter(needed__kittype=kittype)
            name = string.ascii_letters[: len(bagtypes_needed)].upper()
            self.kits.append(
                Kit.objects.create(
                    name=name,
                    quantity=10,
                    complete=True,
                    kind=kittype,
                )
            )

    def test_dividekit_kit0_quantity_1(self):
        PART_ID = 0
        quantity = 1
        original_quantity = self.kits[0].quantity
        response = self.client.put(
            reverse(self.route), {"kit": self.kits[0].pk, "quantity": 1}
        )
        print(response.data)
        self.assertNotEqual(response.data[0]["id"], response.data[1]["id"])
        self.assertEqual(response.data[0]["name"], response.data[1]["name"])
        self.assertEqual(response.data[0]["kind"], response.data[1]["kind"])
        self.assertEqual(response.data[0]["quantity"], original_quantity - quantity)
        self.assertEqual(response.data[1]["quantity"], quantity)

        # Test models in DB
        old_kit = Kit.objects.get(pk=response.data[0]["id"])
        new_kit = Kit.objects.get(pk=response.data[1]["id"])

        self.assertEqual(old_kit.name, new_kit.name)
        self.assertEqual(old_kit.kind, new_kit.kind)
        self.assertEqual(old_kit.complete, new_kit.complete)
        self.assertEqual(old_kit.quantity, original_quantity - quantity)
        self.assertEqual(new_kit.quantity, quantity)
