from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.exceptions import ValidationError, FieldError

from files_logs.models import Action, File, FileJob
from files_logs.serializer import ActionSerializer, FileSerializer, FileJobSerializer
from jobs.models import job
from jobs.serializer import JobSerializer


class ActionsListView(generics.ListAPIView):
    queryset = Action.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ActionSerializer
    filterset_fields = '__all__'

    def paginate_queryset(self, queryset):
        if 'page' not in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)


class FileListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FileSerializer
    filterset_fields = '__all__'

    def get_queryset(self):
        action_id = self.kwargs.get('action_id', None)
        return File.objects.filter(action_id=action_id)

    def paginate_queryset(self, queryset):
        if 'page' not in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)


class FileJobListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = JobSerializer
    filterset_fields = '__all__'
    
    def get_queryset(self):
        file_id = self.kwargs.get('file_id', None)
        fjobs = FileJob.objects.filter(file_id=file_id)
        return job.objects.filter(pk__in=[f.job_id for f in fjobs])

    def paginate_queryset(self, queryset):
        if 'page' not in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)