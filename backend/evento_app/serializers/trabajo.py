from rest_framework import serializers
from ..models import Trabajo

class TrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajo
        fields = '__all__'