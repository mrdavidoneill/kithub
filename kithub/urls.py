from django.urls import include, path
from rest_framework import routers
from .router import router
from .api import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("dividebag/", views.dividebag, name="dividebag"),
    # path("dividekit/", views.dividekit),
    path("potentialkits/<int:kittype>/", views.potentialkits),
    path("potentialkits/", views.all_potentialkits, name="allpotentialkits"),
    path("potentialbags/<int:bagtype>", views.potentialbags),
    path("potentialbags/", views.all_potentialbags, name="allpotentialbags"),
    path(
        "partstobuyforkit/<int:kittype>/<int:quantity>",
        views.partstobuyforkit,
        name="partstobuyforkit",
    ),
    path(
        "partstobuyforbag/<int:bagtype>/<int:quantity>",
        views.partstobuyforbag,
        name="partstobuyforbag",
    ),
    path("unfinishedbag/<int:bagtype>", views.unfinishedbag, name="unfinishedbag"),
    path("unfinishedbag/", views.all_unfinishedbags, name="allunfinishedbags"),
]
