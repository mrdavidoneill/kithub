from kithub.api.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register("kit", KitViewSet)
router.register("kittype", KitTypeViewSet)
router.register("bag", BagViewSet)
router.register("bagtype", BagTypeViewSet)
router.register("part", PartViewSet)
router.register("purchase", PurchaseViewSet)
