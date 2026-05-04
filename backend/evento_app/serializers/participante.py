from rest_framework import serializers
from ..models import Participante

class ParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = '__all__'