from rest_framework import serializers
from files_logs.models import Action, File, FileJob


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class FileJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileJob
        fields = '__all__'
