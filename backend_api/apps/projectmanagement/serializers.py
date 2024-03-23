from rest_framework import serializers

from apps.core.serializers import JobsSerializer
from apps.buyer.serializers import CompanyListSerializer
from .models import (
    Timeline, Meeting
)

class TimelineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timeline
        fields = [
            "id",
            "company",
            "job",
            "approved_gantt_chart",
            "actual_gantt_chart",
            "start_date",
            "end_date",
        ]

class TimelineListSerializer(serializers.ModelSerializer):
    job = JobsSerializer()
    company = CompanyListSerializer()

    class Meta:
        model = Timeline
        fields = [
            "id",
            "company",
            "job",
            "approved_gantt_chart",
            "actual_gantt_chart",
            "start_date",
            "end_date",
        ]

class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = [
            "id",
            "company",
            "job",
            "meeting_minutes",
            "date",
        ]

class MeetingListSerializer(serializers.ModelSerializer):
    job = JobsSerializer()
    company = CompanyListSerializer()

    class Meta:
        model = Meeting
        fields = [
            "id",
            "company",
            "job",
            "meeting_minutes",
            "date",
        ]