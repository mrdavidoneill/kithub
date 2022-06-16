import datetime
from django.test import TestCase
from kithub.api.tests.common import *


class KitTest(TestCase):
    """Test module for Kit model"""

    def setUp(self):
        self.kit = create_kit()

    def test_kit(self):
        retrieve_by_pk(self, Kit, self.kit)


class KitTypeTest(TestCase):
    """Test module for KitType model"""

    def setUp(self):
        self.kittype = create_kittype()

    def test_kittype(self):
        retrieve_by_pk(self, KitType, self.kittype)


class BagTest(TestCase):
    """Test module for Bag model"""

    def setUp(self):
        self.bag = create_bag()

    def test_bag(self):
        retrieve_by_pk(self, Bag, self.bag)


class BagTypeTest(TestCase):
    """Test module for BagType model"""

    def setUp(self):
        self.bagtype = create_bagtype()

    def test_bagtype(self):
        retrieve_by_pk(self, BagType, self.bagtype)


class PartTest(TestCase):
    """Test module for Part model"""

    def setUp(self):
        self.part = create_part()

    def test_part(self):
        retrieve_by_pk(self, Part, self.part)


class PurchaseTest(TestCase):
    """Test module for Purchase model"""

    def setUp(self):
        self.purchase = create_purchase()

    def test_purchase(self):
        retrieve_by_pk(self, Purchase, self.purchase)
