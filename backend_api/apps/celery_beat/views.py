from django import views
from celery import current_app
from celery.utils import cached_property
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from  rest_framework import mixins
from rest_framework.generics import CreateAPIView
from django_celery_beat.models import PeriodicTask
from sqlalchemy import true
from .serializers import PeriodicTaskSerializer, CrontabScheduleSerializer, ClockedScheduleSerializer, IntervalScheduleSerializer ,FetchPeriodicSchedulerSerializer
from  django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule, ClockedSchedule


class PeriodicTaskView(APIView):
    """
    Periodic task
    """
    serializer_class = PeriodicTaskSerializer


    def post(self, request, *args, **kwargs):
        request_data = request.data
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
    
    # def get(self, request, *args, **kwargs):
    #     queryset = PeriodicTask.objects.all()
    #     return Response(self.serializer_class(queryset, many=True).data)

class FetchPeriodicTaskView(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    
    celery_app = current_app
    _options = None

    def get_serializer_class(self):
        return FetchPeriodicSchedulerSerializer

    def get_queryset(self):
        return  PeriodicTask.objects.all()
    
    def tasks_as_options(self):
        _ = self._modules  # noqa
        tasks = list(sorted(name for name in self.celery_app.tasks
                            if not name.startswith('celery.')))
        return (('', ''), ) + tuple(zip(tasks, tasks))

    @property
    def choices(self):
        if self._options is None:
            self._options = self.tasks_as_options()
        return self._options
    
    @cached_property
    def _modules(self):
        self.celery_app.loader.import_default_modules()

    @action(methods=['get'], detail=False, url_path='celery/task-names')
    def task_names(self, request, job_id):
        """Lets you choose between task names."""
        data = self.choices
        return Response(data, status=status.HTTP_200_OK)

    
class CrontabScheduleView(viewsets.ModelViewSet):
    
    def get_serializer_class(self):
        return CrontabScheduleSerializer

    def get_queryset(self):
        return CrontabSchedule.objects.all()

class ClockedScheduleView(viewsets.ModelViewSet):
    
    def get_serializer_class(self):
        return ClockedScheduleSerializer

    def get_queryset(self):
        return ClockedSchedule.objects.all()

class ClockedScheduleView(viewsets.ModelViewSet):
    
    def get_serializer_class(self):
        return ClockedScheduleSerializer

    def get_queryset(self):
        return ClockedSchedule.objects.all()

class IntervalScheduleView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return IntervalScheduleSerializer

    def get_queryset(self):
        return IntervalSchedule.objects.all()

class IntervalScheduleView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return IntervalScheduleSerializer

    def get_queryset(self):
        return IntervalSchedule.objects.all()