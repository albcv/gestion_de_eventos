from rest_framework import serializers
from ..models import EventoTematica

class EventoTematicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoTematica
        fields = '__all__'