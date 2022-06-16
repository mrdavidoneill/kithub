import json
from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import status

from kithub.api.models import *
from kithub.api.serializers import *
from kithub.api.tests import common


class GetAllPotentialKits(TestCase):
    """Test module for retrieving all potential kits"""

    def setUp(self):

        self.route = "unfinishedbag"
        self.client = APIClient()

        # Create stock

        # Create 10 parts with 10 quantity of each
        self.parts = []
        for i in range(10):
            self.parts.append(
                Part.objects.create(
                    name=f"part{i}",
                    description=f"description for part{i}",
                    quantity=0,
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
        print(self.parts)
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
            name = " " * len(parts_needed)
            self.bags.append(
                Bag.objects.create(
                    name=name,
                    quantity=10,
                    complete=False,
                    kind=bagtype,
                )
            )

        self.kits = []

    def test_get_parts_to_buy_for_10_bagtype0_with_nothing_in_bags_10_parts(self):
        BAGTYPE_ID = 0
        for part in self.parts:
            part.increment(10)
        response = self.client.get(
            reverse(self.route, args=(self.bagtypes[BAGTYPE_ID].pk,))
        )
        print(f"response.data: {response.data}")
        expected_to_buy = {}
        expected_to_finish = {part.name: 10 for part in self.parts}
        self.assertEqual(response.data["parts_to_buy"], expected_to_buy)
        self.assertEqual(response.data["parts_to_finish"], expected_to_finish)

    def test_get_parts_to_buy_for_10_bagtype0_with_nothing_in_bags_no_parts(self):
        BAGTYPE_ID = 0
        response = self.client.get(
            reverse(self.route, args=(self.bagtypes[BAGTYPE_ID].pk,))
        )
        print(f"response.data: {response.data}")
        expected_to_buy = {part.name: 10 for part in self.parts}
        expected_to_finish = {part.name: 10 for part in self.parts}
        self.assertEqual(response.data["parts_to_buy"], expected_to_buy)
        self.assertEqual(response.data["parts_to_finish"], expected_to_finish)

    def test_get_parts_to_buy_for_10_bagtype0_with_partA_in_bags_no_parts(self):
        self.bags[0].add_part("A")
        BAGTYPE_ID = 0
        response = self.client.get(
            reverse(self.route, args=(self.bagtypes[BAGTYPE_ID].pk,))
        )
        print(f"response.data: {response.data}")
        expected_to_buy = {part.name: 10 for part in self.parts[1:]}
        expected_to_finish = {part.name: 10 for part in self.parts[1:]}
        self.assertEqual(response.data["parts_to_buy"], expected_to_buy)
        self.assertEqual(response.data["parts_to_finish"], expected_to_finish)

        self.bags[0].remove_part("A")
        response = self.client.get(
            reverse(self.route, args=(self.bagtypes[BAGTYPE_ID].pk,))
        )
        print(f"response.data: {response.data}")
        expected_to_buy = {part.name: 10 for part in self.parts}
        expected_to_finish = {part.name: 10 for part in self.parts}
        self.assertEqual(response.data["parts_to_buy"], expected_to_buy)
        self.assertEqual(response.data["parts_to_finish"], expected_to_finish)
