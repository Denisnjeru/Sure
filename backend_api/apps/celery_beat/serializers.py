from pyexpat import model
import random
import string

from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers
from  django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule, ClockedSchedule

class PeriodicTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = '__all__'
        depth = 1

class IntervalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = '__all__'
        depth = 1 

class CrontabScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrontabSchedule
        fields = [
            'id', 'minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year',
        ]
        depth = 1

class SolarScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarSchedule
        fields = '__all__'
        depth = 1

class ClockedScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClockedSchedule
        fields = '__all__'
        depth = 1

class FetchPeriodicSchedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = ['id', 'name', 'task', 'interval', 'crontab', 'clocked', 'args', 'kwargs', 'queue', 
                'priority', 'expires', 'expire_seconds', 'one_off', 'start_time', 'enabled', 'last_run_at',
                'total_run_count', 'date_changed', 'description']
        