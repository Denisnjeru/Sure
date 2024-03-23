from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
import boto3
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.generics import CreateAPIView
from .models import Notifications
from .serializers import *
from .sqs_resource import tendersure_sqs
from  .s3_resource import tendersure_s3
from django.core.mail import send_mail
from django.template.loader import render_to_string

class UnreadNotificationsList(ViewSet):
    serializer_class = NotificationSerializer

    def list(self, request, *args, **kwargs):
        queryset = Notifications.objects.filter(recipient_id=request.user.id, unread=True)
        return Response(NotificationSerializer(queryset, many=True).data)


class MarkAllAsRead(APIView):
    serializer_class = NotificationSerializer

    def get(self, request, format=None):
        queryset = Notifications.objects.filter(recipient_id=request.user.id, unread=True)
        queryset.update(unread=False)
        return Response({'code': 'OK'}, status=status.HTTP_200_OK)


class MarkAsRead(APIView):
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        notification_id = kwargs.get('slug')
        notification_obj = Notifications.objects.get(id=notification_id)
        notification_obj.unread = False
        notification_obj.save()
        return Response({'code': 'OK'}, status=status.HTTP_200_OK)


class MarkAsUnread(APIView):
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        notification_id = kwargs.get('slug')
        notification_obj = Notifications.objects.get(id=notification_id)
        notification_obj.unread = True
        notification_obj.save()
        return Response({'code': 'OK'}, status=status.HTTP_200_OK)


class Delete(APIView):
    serializer_class = NotificationSerializer

    def delete(self, request, *args, **kwargs):
        notification_id = kwargs.get('slug')
        notification_obj = Notifications.objects.get(id=notification_id)
        notification_obj.delete()
        return Response({'code': 'OK'}, status=status.HTTP_200_OK)


class AddNotification(CreateAPIView):
    serializer_class = NotificationSerializer

    def create(self, request, *args, **kwargs):
        response = super(AddNotification, self).create(request, *args, **kwargs)
        return response


class AllNotification(ViewSet):
    serializer_class = NotificationSerializer

    def list(self, request, *args, **kwargs):
        queryset = Notifications.objects.filter(recipient_id=request.user.id)
        return Response(NotificationSerializer(queryset, many=True).data)


class UnreadNotificationCount(APIView):
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        queryset = Notifications.objects.filter(recipient_id=request.user.id, unread=True)
        count = queryset.count()
        data = {
            'unread_count': count
        }
        return Response(data)


class AllNotificationCount(APIView):
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        queryset = Notifications.objects.filter(recipient_id=request.user.id)
        count = queryset.count()
        data = {
            'all_count': count
        }
        return Response(data)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notifications.objects.all()


    @action(methods=['get'], detail=False, url_path='testaws')
    def testaws(self, request):
        # for bucket in tendersure_s3.buckets.all():
        #     print(bucket.name)

        message = render_to_string(
            "emails/test.html",
            {
                "supplier": 'Supplier',
                "company": 'Denis',
                "category": 'This is a test',
            },
        )

        send_mail(
            'Subject here',
            '',
            'njerudenis@qedsolutions.co.ke',
            ['njerudenis@qedsolutions.co.ke',],
            html_message=message,
            fail_silently=False,
        )
        
        return Response('Printing')