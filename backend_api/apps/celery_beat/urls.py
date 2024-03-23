from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = "celery_beat"
router = DefaultRouter()


router.register(r'crontab-schedules/(?P<job_id>\d+)', CrontabScheduleView, basename='CrontabSchedule')
router.register(r'clocked-schedules/(?P<job_id>\d+)', ClockedScheduleView, basename='ClockedSchedule')
router.register(r'interval-schedules/(?P<job_id>\d+)', ClockedScheduleView, basename='IntervalSchedule')
router.register(r'fetch-periodic-tasks/(?P<job_id>\d+)', FetchPeriodicTaskView, basename='FetchPeriodicTask')

urlpatterns = [
    path('', include(router.urls)),
    path("periodic-tasks/", PeriodicTaskView.as_view(), name='periodic-tasks'),
]