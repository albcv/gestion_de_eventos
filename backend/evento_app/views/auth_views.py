from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from ..serializers import UserSerializer
from ..authentication import CookieTokenAuthentication  

@api_view(['POST'])
@csrf_exempt
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"Error": "Contraseña no válida"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    
    response = Response({"user": serializer.data}, status=status.HTTP_200_OK)
    response.set_cookie(
        key='auth_token',
        value=token.key,
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        max_age=60 * 60 * 24 * 7,
    )
    get_token(request)  # Asegurar cookie CSRF
    return response

@api_view(['POST'])
@csrf_exempt
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
        response = Response({'user': user_data}, status=status.HTTP_201_CREATED)
        response.set_cookie(
            key='auth_token',
            value=token.key,
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=60 * 60 * 24 * 7,
        )
        get_token(request)
        return response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    response = Response({"message": "Sesión cerrada correctamente"}, status=status.HTTP_200_OK)
    response.delete_cookie('auth_token')
    return response

@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def perfil_usuario(request):
    user = request.user
    data = {
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined.strftime('%Y-%m-%d'),
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def cambiar_password(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    if not current_password or not new_password:
        return Response({"error": "Faltan campos"}, status=status.HTTP_400_BAD_REQUEST)
    if not user.check_password(current_password):
        return Response({"error": "Contraseña actual incorrecta"}, status=status.HTTP_400_BAD_REQUEST)
    if len(new_password) < 6:
        return Response({"error": "La nueva contraseña debe tener al menos 6 caracteres"}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(new_password)
    user.save()
    return Response({"message": "Contraseña cambiada correctamente"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@csrf_exempt
def set_csrf_cookie(request):
    get_token(request)
    return Response({"detail": "CSRF cookie establecida"}, status=200)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def health_check(request):
    return Response({"status": "ok"}, status=200)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def keep_alive(request):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1;")
        cursor.fetchone()
    return Response({"status": "ok", "db": "alive"}, status=200)