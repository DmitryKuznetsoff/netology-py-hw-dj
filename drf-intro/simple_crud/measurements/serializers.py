# TODO: опишите сериализаторы
from rest_framework import serializers

from measurements.models import Project, Measurement


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'latitude', 'longitude', 'created_at', 'updated_at',)


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('value', 'project', 'created_at', 'updated_at', 'image')
