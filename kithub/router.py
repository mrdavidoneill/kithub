from kithub.api.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register("kit", KitViewSet)
