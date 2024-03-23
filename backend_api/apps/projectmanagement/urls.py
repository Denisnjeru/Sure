from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.projectmanagement import views

# app_name = "suppliers"
app_name = "projectmanagement"
router = DefaultRouter()

router.register(r"timelines", views.TimelineView, basename="TimelineView")
router.register(r"meetings", views.MeetingView, basename="MeetingView")

urlpatterns = [
    path("", include(router.urls)),
]
