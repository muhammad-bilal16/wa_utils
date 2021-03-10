from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from django.core.exceptions import FieldError

from jobs.models import job
from reporting.models import Service
from reporting.serializer import ServiceSerializer
from reporting.utils.float_arithmetic import multiply_float, add_float, sub_float

from datetime import datetime


class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ServiceSerializer
    filterset_fields = '__all__'

    def paginate_queryset(self, queryset):
        if 'page' not in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ReportByJob(request, notification_no):
    if notification_no:
        j = job.objects.filter(notification_no=notification_no).first()
        if not j:
            return Response('Invalid notification #. Job not found.', status=status.HTTP_400_BAD_REQUEST)

        job_status = j.job_status
        if job_status not in ['Completed', 'Archived']:
            return Response('Report can not be generated. Job not completed.', status=status.HTTP_400_BAD_REQUEST)

        services = j.services.all()
        report_rows = []

        total_wa_utils, total_subby = j.calculated_rates
        data = {
            'notification_no': j.notification_no,
            'job_type': j.job_type,
            'task_completion_date': j.task_completion_date,
            'assigned_to': j.assigned_to,
            'total_wa_utils': total_wa_utils,
            'total_subby': total_subby,
            'total': total_wa_utils + total_subby,
            'services': []
        }

        for s in services:
            data['services'].append({
                'service_code': s.service.code,
                'service_desc': s.service.service_description,
                'quantity': s.quantity,
                'wa_utils_rate': multiply_float(s.quantity, s.service.wa_utilities_rate),
                'subby_rate': multiply_float(s.quantity, s.service.subby_rate)
            })

        return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ReportByDateRange(request):
    # Get date range from request params
    try:
        start_date, end_date = get_date_params(request.GET)
    except ValueError:
        return Response('Invalid start or end date format provided.', status=status.HTTP_400_BAD_REQUEST)

    # Get queryset
    jobs = job.objects.filter(
        task_completion_date__gte=start_date,
        task_completion_date__lte=end_date,
        job_status__in=['Completed', 'Archived']
    )
    
    # If the request is only for the grand total
    if request.GET.get('grand_total_only', 'false') == 'true':
        grand_total_wa_utils = 0
        grand_total_subby = 0
        
        for j in jobs:
            wa_utils, subby = j.calculated_rates
            grand_total_wa_utils = add_float(grand_total_wa_utils, wa_utils)
            grand_total_subby = add_float(grand_total_subby, subby)
        
        return Response({
            'grand_total_wa_utils': grand_total_wa_utils,
            'grand_total_subby': grand_total_subby,
            'grand_total': sub_float(grand_total_wa_utils, grand_total_subby)
        })
    
    # Else if the request is to get a (possibly paginated) list of jobs and their reports
    else:
        count = jobs.count()

        if 'ordering' in request.GET.keys():
            try:
                order = get_sorting_params(request.GET)
                jobs = jobs.order_by(*order)
            except FieldError:
                return Response('Invalid sorting parameters.', status=status.HTTP_400_BAD_REQUEST)

        # If the request requires pagination
        if 'page' in request.GET.keys():
            try:
                page, offset, limit = get_pagination_params(request.GET)
                if page < 1:
                    return Response('Invalid page param. Must be integer greater than 0.', status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response('Invalid page or limit query param. Must be integer.', status=status.HTTP_400_BAD_REQUEST)
            jobs = jobs[offset : offset + limit]

        all_data = {
            'count': count,
            'jobs': [],
        }

        for j in jobs:
            services = j.services.all()
            report_rows = []

            total_wa_utils, total_subby = j.calculated_rates
            job_data = {
                'notification_no': j.notification_no,
                'task_completion_date': j.task_completion_date,
                'job_type': j.job_type,
                'assigned_to': j.assigned_to,
                'total_wa_utils': total_wa_utils,
                'total_subby': total_subby,
                'total': total_wa_utils + total_subby,
                'services': []
            }

            for s in services:
                job_data['services'].append({
                    'service_code': s.service.code,
                    'service_desc': s.service.service_description,
                    'quantity': s.quantity,
                    'wa_utils_rate': multiply_float(s.quantity, s.service.wa_utilities_rate),
                    'subby_rate': multiply_float(s.quantity, s.service.subby_rate)
                })

            all_data['jobs'].append(job_data)

        return Response(all_data)


def get_pagination_params(data):
    page = abs(int(data.get('page', '1')))
    limit = abs(int(data.get('limit', settings.REST_FRAMEWORK.get('PAGE_SIZE', 100))))
    offset = (page - 1) * limit
    return (page, offset, limit)


def get_date_params(data):
    raw_start_date = data.get('start_date', '')
    raw_end_date = data.get('end_date', '')

    start_date = datetime.strptime(raw_start_date, '%Y-%m-%d')
    end_date = datetime.strptime(raw_end_date, '%Y-%m-%d')

    return (start_date, end_date)


# Get query params
def get_sorting_params(data):
    params = data.get('ordering', '').split(',')
    return params
