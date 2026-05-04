from rest_framework import serializers
from ..models import Oponente

class OponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oponente
        fields = '__all__'