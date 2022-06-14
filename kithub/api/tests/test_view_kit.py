from . import common, template_test_view
from ..models import Kit
from ..serializers import KitSerializer

#######################################################
#              Change for each new model              #
#######################################################

ROUTE_LIST = "kit-list"
ROUTE_DETAIL = "kit-detail"
MODEL = Kit
SERIALIZER = KitSerializer

PAYLOAD = common.create_kit_payload


CREATE_ITEM = common.create_kit

#######################################################
#               Same for each model               #
#######################################################

TEST_SETTINGS = {
    "create_item": CREATE_ITEM,
    "model": MODEL,
    "serializer": SERIALIZER,
    "route_list": ROUTE_LIST,
    "route_detail": ROUTE_DETAIL,
    "payload": PAYLOAD,
}


class GetAllItemsTest(template_test_view.GetAllModelsTest):
    """Test module for retrieving all records"""

    def setUp(self):
        self.insert_settings(**TEST_SETTINGS)


class GetASingleItemTest(template_test_view.GetASingleModelTest):
    """Test module for retrieving a single item record"""

    def setUp(self):
        self.insert_settings(**TEST_SETTINGS)


class CreateNewItemTest(template_test_view.CreateNewModelTest):
    """Test module for inserting a new item record"""

    def setUp(self):
        self.insert_settings(**TEST_SETTINGS)


class UpdateSingleItemTest(template_test_view.UpdateSingleModelTest):
    """Test module for updating an existing item record"""

    def setUp(self):
        self.insert_settings(**TEST_SETTINGS)


class DeleteSingleItemTest(template_test_view.DeleteSingleModelTest):
    """Test module for deleting an existing item record"""

    def setUp(self):
        self.insert_settings(**TEST_SETTINGS)
