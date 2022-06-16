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

        self.route = "partstobuyforkit"
        self.client = APIClient()

        # Create stock

        # Create 10 parts with 0 quantity of each
        self.parts = []
        for i in range(10):
            self.parts.append(
                Part.objects.create(
                    name=f"part{i}",
                    description=f"description for part{i}",
                    quantity=0,
                )
            )
        print(self.parts)
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
        for i, part in enumerate(self.parts):
            BagIngredient.objects.create(
                name=string.ascii_letters[i].upper(),
                bagtype=self.bagtypes[0],
                part=part,
                quantity=1,
            )

        print(self.parts)
        # Create bagingredients for bagtype1
        # 2 of each part
        for i, part in enumerate(self.parts):
            BagIngredient.objects.create(
                name=string.ascii_letters[i].upper(),
                bagtype=self.bagtypes[1],
                part=part,
                quantity=2,
            )

        # Create bagingredients for bagtype2
        # 1 of first two parts
        for i, part in enumerate(self.parts[:2]):
            BagIngredient.objects.create(
                name=string.ascii_letters[i].upper(),
                bagtype=self.bagtypes[2],
                part=part,
                quantity=1,
            )

        # Create kitingredients for kittype0
        # 1 of each bagtype

        for i, bagtype in enumerate(self.bagtypes):
            KitIngredient.objects.create(
                name=string.ascii_letters[i].upper(),
                kittype=self.kittypes[0],
                bagtype=bagtype,
                quantity=1,
            )

        # Create kitingredients for kittype1
        # 2 of each bagtype
        for i, bagtype in enumerate(self.bagtypes):
            KitIngredient.objects.create(
                name=string.ascii_letters[i].upper(),
                kittype=self.kittypes[1],
                bagtype=bagtype,
                quantity=2,
            )

        # Create kitingredients for kittype2
        # 1 of first two parts
        for i, bagtype in enumerate(self.bagtypes[:2]):
            KitIngredient.objects.create(
                name=string.ascii_letters[i].upper(),
                kittype=self.kittypes[2],
                bagtype=bagtype,
                quantity=1,
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

    def test_get_parts_to_buy_for_10_kittype0_with_10(self):

        # 10 of each part for bag0
        # 20 of each part for bag1
        # 10 of first two parts for bag2
        # stock enough parts for bag0 already
        [part.increment(10) for part in self.parts]

        KITTYPE_ID = 0
        response = self.client.get(
            reverse(self.route, args=(self.kittypes[KITTYPE_ID].pk, 10))
        )
        print(response.data)

        # parts for bag1
        expected = {part.name: 20 for part in self.parts}
        # parts for bag2
        expected[self.parts[0].name] += 10
        expected[self.parts[1].name] += 10

        self.assertEqual(response.data["parts_to_buy"], expected)

    def test_get_parts_to_buy_for_10_kittype0_with_nothing(self):
        KITTYPE_ID = 0
        response = self.client.get(
            reverse(self.route, args=(self.kittypes[KITTYPE_ID].pk, 10))
        )
        print(response.data)

        # 10 of each part for bag0
        # 20 of each part for bag1
        # 10 of first two parts for bag2

        # parts for bag0 and bag1
        expected = {part.name: 10 + 20 for part in self.parts}
        # parts for bag2
        expected[self.parts[0].name] += 10
        expected[self.parts[1].name] += 10

        self.assertEqual(response.data["parts_to_buy"], expected)

    def test_get_parts_to_buy_for_10_kittype0_with_only_part0(self):

        [part.increment(10) for part in self.parts[:1]]

        KITTYPE_ID = 0
        response = self.client.get(
            reverse(self.route, args=(self.kittypes[KITTYPE_ID].pk, 10))
        )
        print(response.data)

        # 10 of each part for bag0
        # 20 of each part for bag1
        # 10 of first two parts for bag2

        # parts for bag0 and bag1
        expected = {part.name: 10 + 20 for part in self.parts}
        # Decrement part0 by 10
        expected[self.parts[0].name] -= 10
        # parts for bag2
        expected[self.parts[0].name] += 10
        expected[self.parts[1].name] += 10

        self.assertEqual(response.data["parts_to_buy"], expected)

    def test_get_parts_to_buy_for_10_kittype0_with_all_plenty(self):

        [part.increment(9999) for part in self.parts]

        KITTYPE_ID = 0
        response = self.client.get(
            reverse(self.route, args=(self.kittypes[KITTYPE_ID].pk, 10))
        )
        print(response.data)

        # 10 of each part for bag0
        # 20 of each part for bag1
        # 10 of first two parts for bag2

        self.assertEqual(response.data["parts_to_buy"], {})

    def test_get_parts_to_buy_for_10_kittype0_with_part0_plenty(self):

        [part.increment(9999) for part in self.parts[0:1]]

        KITTYPE_ID = 0
        response = self.client.get(
            reverse(self.route, args=(self.kittypes[KITTYPE_ID].pk, 10))
        )
        print(response.data)

        # 10 of each part for bag0
        # 20 of each part for bag1
        # 10 of first two parts for bag2

        # parts for bag0 and bag1
        expected = {part.name: 10 + 20 for part in self.parts[1:]}

        # parts for bag2
        expected[self.parts[1].name] += 10
        self.assertEqual(response.data["parts_to_buy"], expected)

    def test_get_parts_to_buy_for_10_kittype0_with_all_plenty_bar_part0(self):

        [part.increment(9999) for part in self.parts[1:]]

        KITTYPE_ID = 0
        response = self.client.get(
            reverse(self.route, args=(self.kittypes[KITTYPE_ID].pk, 10))
        )
        print(response.data)

        # 10 of each part for bag0
        # 20 of each part for bag1
        # 10 of first two parts for bag2

        # parts for bag0 and bag1
        expected = {self.parts[0].name: 10 + 20}

        # parts for bag2
        expected[self.parts[0].name] += 10
        self.assertEqual(response.data["parts_to_buy"], expected)
