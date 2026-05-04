from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Evento
from ..authentication import CookieTokenAuthentication

@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def evento_actual(request):
    try:
        evento = Evento.objects.order_by('-fecha_apertura').first()
        if not evento:
            return Response({"error": "No hay eventos registrados"}, status=404)

        tematicas = list(evento.tematicas.all().values('id', 'nombre'))

        user = request.user
        rol = None
        if hasattr(user, 'participante_profile'):
            rol = 'participante'
        elif hasattr(user, 'oponente_profile'):
            rol = 'oponente'

        data = {
            'id': evento.id,
            'nombre': evento.nombre,
            'fecha_apertura': evento.fecha_apertura.isoformat(),
            'fecha_cierre': evento.fecha_cierre.isoformat(),
            'entidad_patrocinadora': evento.id_entidad.nombre,
            'tematicas': tematicas,
            'rol_usuario': rol,
        }
        return Response(data, status=200)
    except Exception as e:
        return Response({"error": f"Error interno: {str(e)}"}, status=500)