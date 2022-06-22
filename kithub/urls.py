from django.urls import include, path
from rest_framework import routers
from .router import router
from .api import views

urlpatterns = [
    # Automatic API URL routing
    path("", include(router.urls)),
    # Web browsable admin API
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # Endpoints for UC25-UC31
    path("dividebag/", views.dividebag, name="dividebag"),  # UC25
    path("dividekit/", views.dividekit, name="dividekit"),  # UC26
    path("potentialkits/<int:kittype>/",
         views.potentialkits, name="potentialkits"),  # UC27
    path("potentialkits/", views.all_potentialkits,
         name="allpotentialkits"),  # UC27
    path("potentialbags/<int:bagtype>",
         views.potentialbags, name="potentialbags"),  # UC28
    path("potentialbags/", views.all_potentialbags,
         name="allpotentialbags"),  # UC28
    path(
        "partstobuyforkit/<int:kittype>/<int:quantity>",
        views.partstobuyforkit,
        name="partstobuyforkit",
    ),  # UC29
    path(
        "partstobuyforbag/<int:bagtype>/<int:quantity>",
        views.partstobuyforbag,
        name="partstobuyforbag",
    ),  # UC30
    path("unfinishedbag/<int:bagtype>",
         views.unfinishedbag, name="unfinishedbag"),  # UC31
    path("unfinishedbag/", views.all_unfinishedbags,
         name="allunfinishedbags"),  # UC31
]
