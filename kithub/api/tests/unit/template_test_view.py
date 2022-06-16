from django.test import TestCase, Client
from rest_framework.test import APIClient

from kithub.api.tests import common

ITEM_COUNT = 2


class GetAllModelsTest(TestCase):
    """Test module template for retrieving all report records"""

    def insert_settings(self, **kwargs):
        """Insert all the required setting values"""
        self.create_item = kwargs["create_item"]
        self.model = kwargs["model"]
        self.serializer = kwargs["serializer"]
        self.route_list = kwargs["route_list"]
        self.route_detail = kwargs["route_detail"]

        self.template_SetUp()

    def template_SetUp(self):
        """Create client
        Create authenticated user & attach their token to client
        Create 2 items with user account
        Create 1 item on another account
        """

        # Create client
        self.client = APIClient()

        # Expect all current items to be returned
        self.expected_count = len(self.model.objects.all())

        # Create new items
        items = []
        for item in range(ITEM_COUNT):
            items.append(self.create_item())

        # Expect new items to be returned too
        self.expected_count += ITEM_COUNT

        # Common settings for all tests
        self.test_settings = {
            "client": self.client,
            "route": self.route_list,
            "instance": self,
            "model": self.model,
            "serializer": self.serializer,
        }

    def test_get_all_items(self):
        """Test that all items are returned
        Will test for: Expected number of results
                       Status code 200
        """
        common.test_get_all(expected_number=self.expected_count, **self.test_settings)


class GetASingleModelTest(TestCase):
    """Test module template for retrieving a single item record"""

    def insert_settings(self, **kwargs):
        """Insert all the required setting values"""
        self.create_item = kwargs["create_item"]
        self.model = kwargs["model"]
        self.serializer = kwargs["serializer"]
        self.route_list = kwargs["route_list"]
        self.route_detail = kwargs["route_detail"]

        self.template_SetUp()

    def template_SetUp(self):
        """Create client"""
        # Create client
        self.client = APIClient()

        self.itemA = self.create_item()
        self.itemB = self.create_item()
        self.itemC = self.create_item()

        self.test_settings = {
            "client": self.client,
            "route": self.route_detail,
            "instance": self,
            "model": self.model,
            "serializer": self.serializer,
        }

    def test_get_item(self):
        """Test that correct item is returned
        Will return a status code 200"""

        common.test_valid_get_single_item(item=self.itemB, **self.test_settings)
        common.test_valid_get_single_item(item=self.itemA, **self.test_settings)
        common.test_valid_get_single_item(item=self.itemC, **self.test_settings)

    def test_get_invalid_item(self):
        """Test that an item is not returned
        Will return a status code 404"""

        common.test_invalid_get_single_item(**self.test_settings)


class CreateNewModelTest(TestCase):
    """Test module template for inserting a new item record"""

    def insert_settings(self, **kwargs):
        """Insert all the required setting values"""
        self.create_item = kwargs["create_item"]
        self.model = kwargs["model"]
        self.serializer = kwargs["serializer"]
        self.route_list = kwargs["route_list"]
        self.route_detail = kwargs["route_detail"]
        self.payload_template = kwargs["payload"]

        self.template_SetUp()

    def template_SetUp(self):
        """Create client
        Create authenticated user & attach their token to client
        Create 1 dictionary with a valid Payload with items on user's account
        Create 1 dictionary with a valid Payload with items on another account
        Create 1 dictionary with a valid Payload with wrong non existing IDs
        """
        self.client = APIClient()

        self.valid_payload = self.payload_template()

        self.empty_payload = {}

        self.test_settings = {
            "client": self.client,
            "route": self.route_list,
            "instance": self,
        }

    def test_create_valid_item(self):
        """Test user can create item into same account with valid payload
        Will create item in the DB
        Will test that status code 201 is returned
        Wll retrieve item by its pk
        Will test that status code 200 is returned
        Will test that the item retrived has the same properties as the item created
        """

        common.test_valid_create(
            payload=self.valid_payload,
            model=self.model,
            serializer=self.serializer,
            detail_route=self.route_detail,
            **self.test_settings
        )

        common.test_empty_create(
            payload=self.empty_payload,
            model=self.model,
            serializer=self.serializer,
            detail_route=self.route_detail,
            **self.test_settings
        )


class UpdateSingleModelTest(TestCase):
    """Test module template for updating an existing item record"""

    def insert_settings(self, **kwargs):
        """Insert all the required setting values"""
        self.create_item = kwargs["create_item"]
        self.model = kwargs["model"]
        self.serializer = kwargs["serializer"]
        self.route_list = kwargs["route_list"]
        self.route_detail = kwargs["route_detail"]
        self.payload_template = kwargs["payload"]

        self.template_SetUp()

    def template_SetUp(self):
        """Create client
        Create authenticated user & attach their token to client
        Create 1 dictionary with a valid Payload with items on user's account
        Create 1 dictionary with a valid Payload with items on another account
        Create 1 dictionary with a valid Payload with wrong non existing IDs
        Create 1 dictionary with an valid Payload with empty IDs
        """
        self.client = APIClient()

        self.valid_payload = self.payload_template()

        self.empty_payload = {}

        self.item = self.create_item()
        self.test_settings = {
            "client": self.client,
            "route": self.route_detail,
            "instance": self,
        }

    def test_valid_update_item(self):
        """Test that user can update item with valid payload
        Wll update existing item by its pk
        Will test that status code 200 is returned
        Will test that the item retrieved has the same properties as the existing item + changed one
        """

        common.test_valid_update(
            item=self.item, payload=self.valid_payload, **self.test_settings
        )
        common.test_empty_update(
            item=self.item, payload=self.empty_payload, **self.test_settings
        )


class DeleteSingleModelTest(TestCase):
    """Test module template for deleting an existing item record"""

    def insert_settings(self, **kwargs):
        """Insert all the required setting values"""
        self.create_item = kwargs["create_item"]
        self.model = kwargs["model"]
        self.serializer = kwargs["serializer"]
        self.route_list = kwargs["route_list"]
        self.route_detail = kwargs["route_detail"]

        self.template_SetUp()

    def template_SetUp(self):
        """Create client
        Create authenticated user & attach their token to client
        Create 2 items with user account
        Create 1 item on another account
        """
        # Create client & authenticate with user
        self.client = APIClient()

        self.itemA = self.create_item()
        self.itemB = self.create_item()
        self.itemC = self.create_item()

        self.test_settings = {
            "client": self.client,
            "route": self.route_detail,
            "route_list": self.route_list,
            "instance": self,
            "model": self.model,
        }

    def test_valid_delete_item(self):
        """Test that user can delete existing item in the same account
        Wll delete existing item by its pk
        Will test that status code 204 is returned
        Will test that the number of items retrived has fallen by one
        Will test retrieving the item again
            Will return status code 404
        """

        common.test_valid_delete(item=self.itemB, **self.test_settings)
