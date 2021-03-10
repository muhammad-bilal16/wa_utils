from jobs.models import job
from django_filters.rest_framework import BaseInFilter, CharFilter, FilterSet


class CharInFilter(BaseInFilter, CharFilter):
    pass


class JobFilter(FilterSet):
    job_type_in = CharInFilter(field_name='job_type', lookup_expr='in')
    job_status_in = CharInFilter(field_name='job_status', lookup_expr='in')

    class Meta:
        model = job
        fields = '__all__'
