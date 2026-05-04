from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from ..models import Participante

class UserSerializer(serializers.ModelSerializer):
  
    nombre = serializers.CharField(max_length=100, write_only=True, required=True)
    apellido1 = serializers.CharField(max_length=100, write_only=True, required=True)
    apellido2 = serializers.CharField(max_length=100, write_only=True, required=True)
    grado_cientifico = serializers.CharField(max_length=50, write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'nombre', 'apellido1', 'apellido2', 'grado_cientifico']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("El nombre de usuario ya existe")
        return value

    def validate_email(self, value):
        # Validar formato de email
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("El email no es válido")
        
        # Verificar que el email no esté ya registrado
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("El email ya está registrado")
        
        return value

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre es obligatorio")
        return value

    def validate_apellido1(self, value):
        if not value.strip():
            raise serializers.ValidationError("El primer apellido es obligatorio")
        return value

    def validate_apellido2(self, value):
        if not value.strip():
            raise serializers.ValidationError("El segundo apellido es obligatorio")
        return value

    def validate_grado_cientifico(self, value):
        if not value.strip():
            raise serializers.ValidationError("El grado científico es obligatorio")
        return value

    def create(self, validated_data):
        # Extraer datos del perfil
        nombre = validated_data.pop('nombre')
        apellido1 = validated_data.pop('apellido1')
        apellido2 = validated_data.pop('apellido2')
        grado_cientifico = validated_data.pop('grado_cientifico')

        # Crear usuario
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Crear perfil Participante
        Participante.objects.create(
            user=user,
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            grado_cientifico=grado_cientifico
        )
        return user