from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = "core"
router = DefaultRouter()

router.register('', NotificationViewSet)

urlpatterns = [
    path("notification/", include(router.urls)), #  No linked to  user id
    path('notification/add/', AddNotification.as_view(), name='add'),
    path('notification/api/all/', AllNotification.as_view({'get': 'list'}), name='all'),
    path('notification/unread/', UnreadNotificationsList.as_view({'get': 'list'}), name='unread'),
    path('notification/mark-all-as-read/', MarkAllAsRead.as_view(), name='mark_all_as_read'),
    path('notification/mark-as-read/<slug>/', MarkAsRead.as_view(), name='mark_as_read'),
    path('notification/mark-as-unread/<slug>/', MarkAsUnread.as_view(), name='mark_as_unread'),
    path('notification/delete/<slug>/', Delete.as_view(), name='delete'),
    path('notification/api/unread_count/', UnreadNotificationCount.as_view(), name='live_unread_notification_count'),
    path('notification/api/all_count/', AllNotificationCount.as_view(), name='live_all_notification_count'),
    path('notification/api/unread_list/', UnreadNotificationsList.as_view({'get': 'list'}), name='live_unread_notification_list'),
]