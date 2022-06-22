from kithub.api.views import *
from rest_framework import routers

# Automatic API CRUD routing (UC1 - UC24)
router = routers.DefaultRouter()
router.register("kit", KitViewSet)
router.register("kittype", KitTypeViewSet)
router.register("bag", BagViewSet)
router.register("bagtype", BagTypeViewSet)
router.register("part", PartViewSet)
router.register("purchase", PurchaseViewSet)
router.register("bagingredient", BagIngredientViewSet)
router.register("kitingredient", KitIngredientViewSet)
