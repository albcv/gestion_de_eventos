from rest_framework import serializers
from ..models import Tematica

class TematicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tematica
        fields = '__all__'