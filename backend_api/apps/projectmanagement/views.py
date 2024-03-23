from django.shortcuts import render
from django import http, apps

from rest_framework import generics, status, views, viewsets
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated

from .serializers import (
    TimelineSerializer, MeetingSerializer, TimelineListSerializer, MeetingListSerializer
)
from .models import (
    Timeline, Meeting
)
from apps.authentication.tokens import get_user_type
from apps.core.pagination import PageNumberPagination


# Create your views here.
class TimelineView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post", "patch", "delete"]
    parser_classes = (MultiPartParser,FormParser,FileUploadParser,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return TimelineListSerializer
        return TimelineSerializer

    def get_queryset(self):
        user_type = get_user_type(self.request.auth.payload['user_id'])
        if user_type == 'buyer':
            return Timeline.objects.filter(company_id=self.request.auth.payload['company_id'])
        else:
            return Timeline.objects.all().order_by("-id")

    def create(self, request, *args, **kwargs):
        user_type = get_user_type(self.request.auth.payload['user_id'])
        if user_type != 'qed':
            return Response({"error": "Invalid action"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MeetingView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post", "patch", "delete"]
    parser_classes = (MultiPartParser,FormParser,FileUploadParser,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return MeetingListSerializer
        return MeetingSerializer

    def get_queryset(self):
        user_type = get_user_type(self.request.auth.payload['user_id'])
        if user_type == 'buyer':
            return Meeting.objects.filter(company_id=self.request.auth.payload['company_id'])
        else:
            return Meeting.objects.all().order_by("-id")

    def create(self, request, *args, **kwargs):
        user_type = get_user_type(self.request.auth.payload['user_id'])
        if user_type != 'qed':
            return Response({"error": "Invalid action"}, status=status.HTTP_403_FORBIDDEN)

        print(request.data['company'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)