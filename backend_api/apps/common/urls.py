from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.common import views

app_name = "common"
router = DefaultRouter()

router.register(r"countries", views.CountryView, basename="CountryView")
router.register(r"locations", views.LocationView, basename="LocationView")
router.register(r"category_types", views.CategoryTypeView, basename="CategoryTypeView")

urlpatterns = [
    path("", include(router.urls)),
]
