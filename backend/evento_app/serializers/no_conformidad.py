from rest_framework import serializers
from ..models import NoConformidad

class NoConformidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoConformidad
        fields = '__all__'