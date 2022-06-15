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

        self.route = "allpotentialbags"
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

        self.kits = []

        print(self.bags)

    def test_get_potentialbags_decrementing_part0(self):
        PART_ID = 0
        response = self.client.get(reverse(self.route))
        print(response.data)
        self.assertEqual(response.data[0]["potential_bags"], 10)
        self.assertEqual(response.data[1]["potential_bags"], 5)
        self.assertEqual(response.data[2]["potential_bags"], 10)

        # Decrease bag0 by 1
        self.parts[PART_ID].decrement()

        response = self.client.get(reverse(self.route))
        print(response.data)
        self.assertEqual(response.data[0]["potential_bags"], 9)
        self.assertEqual(response.data[1]["potential_bags"], 4)
        self.assertEqual(response.data[2]["potential_bags"], 9)

        # Increase bag0 by 1
        self.parts[PART_ID].increment()

        response = self.client.get(reverse(self.route))
        print(response.data)
        self.assertEqual(response.data[0]["potential_bags"], 10)
        self.assertEqual(response.data[1]["potential_bags"], 5)
        self.assertEqual(response.data[2]["potential_bags"], 10)

    def test_get_potentialbags_decrementing_part2(self):
        PART_ID = 2
        response = self.client.get(reverse(self.route))
        print(response.data)
        self.assertEqual(response.data[0]["potential_bags"], 10)
        self.assertEqual(response.data[1]["potential_bags"], 5)
        self.assertEqual(response.data[2]["potential_bags"], 10)

        # Decrease bag0 by 2
        self.parts[PART_ID].decrement(2)

        response = self.client.get(reverse(self.route))
        print(response.data)
        self.assertEqual(response.data[0]["potential_bags"], 8)
        self.assertEqual(response.data[1]["potential_bags"], 4)
        self.assertEqual(response.data[2]["potential_bags"], 10)

        # Increase bag0 by 1
        self.parts[PART_ID].increment(2)

        response = self.client.get(reverse(self.route))
        print(response.data)
        self.assertEqual(response.data[0]["potential_bags"], 10)
        self.assertEqual(response.data[1]["potential_bags"], 5)
        self.assertEqual(response.data[2]["potential_bags"], 10)
