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

        self.route = "allpotentialkits"
        self.client = APIClient()

        # Create stock

        # Create parts
        self.parts = []
        for i in range(2):
            self.parts.append(
                Part.objects.create(
                    name=f"part{i}",
                    description=f"description for part{i}",
                    quantity=i * 10,
                )
            )
        # Create bagtypes
        self.bagtypes = []
        for i in range(2):
            self.bagtypes.append(BagType.objects.create(kind=f"bagtype{i}"))

        # Create bagtypes
        self.kittypes = []
        for i in range(2):
            self.kittypes.append(KitType.objects.create(kind=f"kittype{i}"))

        # Create bagingredients
        self.bagingredients = []
        for index, bagtype in enumerate(self.bagtypes):
            for i, part in enumerate(self.parts[index:]):
                self.bagingredients.append(
                    BagIngredient.objects.create(
                        name=string.ascii_letters[i].upper(),
                        bagtype=bagtype,
                        part=part,
                        quantity=index + 1,
                    )
                )

        self.kitingredients = []

        # Create kitingredients
        self.kitingredients = []
        for index, kittype in enumerate(self.kittypes):
            for i, bagtype in enumerate(self.bagtypes[index:]):
                self.kitingredients.append(
                    KitIngredient.objects.create(
                        name=string.ascii_letters[i].upper(),
                        kittype=kittype,
                        bagtype=bagtype,
                        quantity=index + 1,
                    )
                )
        self.bags = []
        self.kits = []

    def test_get_potentialkits_with_no_bags(self):

        response = self.client.get(reverse(self.route))
        print(response.data)
        self.assertEqual(response.data[0]["potential_kits"], 0)

    def test_get_potentialkits_with_single_bags(self):

        response = self.client.get(reverse(self.route))
        print(response.data)
        self.assertEqual(response.data[0]["potential_kits"], 1)
