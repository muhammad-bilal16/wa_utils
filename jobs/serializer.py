from rest_framework import serializers
from jobs.models import job, JobActivity, JobService
from reporting.serializer import ServiceSerializer

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = job
        fields = '__all__'


class JobActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobActivity
        fields = '__all__'


class JobServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobService
        fields = '__all__'


class JobServiceDetailSerializer(serializers.ModelSerializer):
    service_details = ServiceSerializer()
    class Meta:
        model = JobService
        fields = ['quantity', 'service_details']
