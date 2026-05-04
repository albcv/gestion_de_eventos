from rest_framework import serializers
from ..models import EventoParticipante

class EventoParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoParticipante
        fields = '__all__'