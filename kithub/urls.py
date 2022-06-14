from django.urls import include, path
from rest_framework import routers
from .router import router
from .api import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # path("dividebag/", views.dividebag),
    # path("dividekit/", views.dividekit),
    path("potentialkits/<int:kittype>/", views.potentialkits),
    path("potentialkits/", views.all_potentialkits, name="allpotentialkits"),
    path("potentialbags/<int:bagtype>", views.potentialbags),
    path("potentialbags/", views.all_potentialbags),
    # path("partstobuyforkit/", views.partstobuyforkit),
    # path("partstobuyforbag/", views.partstobuyforbag),
    # path("unfinishedbag/<int:bag>", views.unfinishedbag),
    # path("unfinishedbag/", views.all_unfinishedbags),
]
