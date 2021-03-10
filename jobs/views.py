from django.db import models

from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from jobs.models import job, JobActivity, JobService
from jobs.serializer import JobSerializer, JobActivitySerializer, JobServiceSerializer, JobServiceDetailSerializer

from reporting.models import Service
from reporting.serializer import ServiceSerializer

from files_logs.models import Action
from jobs.imports import job_import
from jobs.exports import job_export
from jobs.utils.custom_filter import JobFilter

from datetime import datetime


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def JobDetailAPI(request, pk):
    try:
        item = job.objects.get(id=pk)
    except job.DoesNotExist:
        Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = JobSerializer(item, many=False)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def JobImportApi(request):
    action = Action.objects.create(
        status='pending', account_id=request.user.email, action_type='import'
    )
    file_list = job_import.import_from_sftp_server(action)
    return Response(file_list)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def JobExportApi(request):
    action = Action.objects.create(
        status='pending', account_id=request.user.email, action_type='export'
    )
    exported_files = job_export.export_to_sftp_server(action)
    return Response(exported_files)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def JobCreateAPI(request):
    if request.user.is_staff:
        if request.method == "POST":
            serializer = JobSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def JobUpdateAPI(request, pk):
    if request.user.is_staff:
        try:
            jobb = job.objects.get(id=pk)
        except job.DoesNotExist:
            return Response('Invalid job ID provided', status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data

        for a in data.get('activities', []):
            try:
                activity = JobActivity.objects.get(job_id=pk, pk=a.get('id', None))
            except JobActivity.DoesNotExist:
                activity = JobActivity.objects.create(job_id=pk)
            except ValueError:
                activity = JobActivity.objects.create(job_id=pk)

            activity.code = a.get('code', '')
            activity.code_group = a.get('code_group', '')
            activity.quantity = a.get('quantity', 0)
            activity.save()
            try:
                if 'start_date' in a.keys():
                    activity.start_date = datetime.strptime(a.get('start_date', ''), '%Y-%m-%d')
                if 'end_date' in a.keys():
                    activity.end_date = datetime.strptime(a.get('end_date', ''), '%Y-%m-%d')
            except ValueError:
                print(f'Start or end date field invalid for activity id: {activity.id}')
                
        data.pop('activities', None)

        if 'services' in data.keys():
            # Getting current services of this job, which will be deleted
            current_services = JobService.objects.filter(job_id=pk)

            # Going through all the latest provided services
            for s in data.get('services', []):
                try:
                    service = Service.objects.get(pk=s.get('id', None))
                except Service.DoesNotExist:
                    return Response('Invalid service code provided for update', status.HTTP_400_BAD_REQUEST)
                    
                try:
                    j_service = JobService.objects.get(job_id=pk, service=service)
                    j_service.quantity = s.get('quantity', 0)
                except JobService.DoesNotExist:
                    j_service = JobService.objects.create(
                        job=jobb, service=service, quantity=s.get('quantity', 0)
                    )

                # Excluding this existing services from the services to be deleted
                current_services = current_services.exclude(id=j_service.id)
                j_service.save()

            data.pop('services', None)
            current_services.delete()

        serializer = JobSerializer(instance=jobb, data=data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "Updated successfully!"
            data["job"] = serializer.data
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def JobBulkUpdateAPI(request):
    if request.user.is_staff:
        if request.data['ids'] and request.data['data']:
            if (validate_ids(request.data['ids'])):
                ids = request.data['ids']
            else:
                return Response('Multiple instances of the same "id" are not allowed')

            data = request.data['data']
            if 'job_status' in data.keys():
                if not validate_job_status(data['job_status']):
                    return Response('Invalid job_status provided')
            
            jobs_to_update = job.objects.filter(id__in=ids)
            jobs_to_update.update(**data)
        else:
            Response('No "ids" found for update', status.HTTP_400_BAD_REQUEST)
        return Response('Updated successfully')
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def JobDeleteAPI(request, pk):
    if request.user.is_staff:
        try:
            jobb = job.objects.get(id=pk)
        except job.DoesNotExist:
            Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == "DELETE":
            operation = jobb.delete()
            data = {}
            if operation:
                data["success"] = "Deleted successfully!"
            else:
                data["failure"] = "Delete failed!"
            return Response(data=data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


class JobListViewset(generics.ListAPIView):
    queryset = job.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_class = JobFilter
    serializer_class = JobSerializer
    filterset_fields = '__all__'
    search_fields = ['notification_no', 'job_status', 'job_type', 'assigned_to', 'functional_loc_desc']

    def paginate_queryset(self, queryset):
        if 'page' not in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)


class JobActivityViewset(generics.ListAPIView):
    queryset = JobActivity.objects.order_by('id')
    serializer_class = JobActivitySerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = '__all__'

    def get_queryset(self,):
        return JobActivity.objects.filter(job_id=self.request.GET['job_id'])

    def paginate_queryset(self, queryset):
        if 'page' not in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)


class JobServiceViewset(generics.ListAPIView):
    serializer_class = JobServiceDetailSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = '__all__'

    def get_queryset(self):
        job_id = self.kwargs.get('job_id', None)
        return JobService.objects.filter(job_id=job_id)

    def paginate_queryset(self, queryset):
        if 'page' not in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)


def validate_ids(ids):
    if isinstance(ids, list):
        return len(ids) == len(set(ids))
    return [ids]


def validate_job_status(status):
    return (status, status) in job._meta.get_field('job_status').choices