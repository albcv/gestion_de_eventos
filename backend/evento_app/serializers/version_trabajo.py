from rest_framework import serializers
from ..models import VersionTrabajo

class VersionTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersionTrabajo
        fields = '__all__'