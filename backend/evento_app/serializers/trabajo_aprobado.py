from rest_framework import serializers
from ..models import TrabajoAprobado

class TrabajoAprobadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrabajoAprobado
        fields = '__all__'