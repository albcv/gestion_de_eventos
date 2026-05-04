import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import FileResponse, Http404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Evento, Tematica, Trabajo, VersionTrabajo, Tribunal, TrabajoAprobado
from ..authentication import CookieTokenAuthentication

@api_view(['POST'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def crear_trabajo(request):
    try:
        participante = request.user.participante_profile
    except AttributeError:
        return Response({"error": "Solo los participantes pueden subir trabajos"}, status=403)

    titulo = request.data.get('titulo')
    tematica_id = request.data.get('tematica_id')
    archivo = request.FILES.get('archivo')
    descripcion = request.data.get('descripcion', '')

    if not titulo or not tematica_id or not archivo:
        return Response({"error": "Faltan campos obligatorios"}, status=400)

    try:
        tematica = Tematica.objects.get(id=tematica_id)
    except Tematica.DoesNotExist:
        return Response({"error": "Temática no válida"}, status=400)

    evento = Evento.objects.order_by('-fecha_apertura').first()
    if not evento:
        return Response({"error": "No hay eventos activos"}, status=404)

    if not evento.eventotematica_set.filter(id_tematica=tematica).exists():
        return Response({"error": "La temática no pertenece al evento actual"}, status=400)

    tribunal = Tribunal.objects.first()
    if not tribunal:
        return Response({"error": "No hay tribunales registrados"}, status=400)

    trabajo = Trabajo.objects.create(
        titulo=titulo,
        evento=evento,
        id_participante=participante,
        id_tematica=tematica,
        id_tribunal=tribunal
    )

    extension = archivo.name.split('.')[-1].lower()
    if extension not in ['pdf', 'doc', 'docx']:
        return Response({"error": "Formato no permitido"}, status=400)

    nombre_base = os.path.splitext(archivo.name)[0]
    nombre_archivo = f"trabajo_{trabajo.id}_v1_{nombre_base}.{extension}"
    carpeta_destino = f"trabajos/evento_{evento.id}/trabajo_{trabajo.id}"
    ruta_completa = default_storage.save(os.path.join(carpeta_destino, nombre_archivo), ContentFile(archivo.read()))
    tamanio_kb = archivo.size // 1024

    version = VersionTrabajo.objects.create(
        trabajo=trabajo,
        version_numero=1,
        archivo=ruta_completa,
        nombre_archivo=nombre_archivo,
        tipo_archivo=extension,
        tamanio=tamanio_kb,
        descripcion=descripcion
    )

    return Response({
        "mensaje": "Trabajo creado exitosamente",
        "trabajo_id": trabajo.id,
        "version": version.version_numero,
        "archivo": version.archivo.url if version.archivo else None
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def obtener_mi_trabajo(request):
    try:
        participante = request.user.participante_profile
    except AttributeError:
        return Response({"error": "Solo participantes"}, status=403)

    evento = Evento.objects.order_by('-fecha_apertura').first()
    if not evento:
        return Response({"error": "No hay evento activo"}, status=404)

    try:
        trabajo = Trabajo.objects.get(id_participante=participante, evento=evento)
    except Trabajo.DoesNotExist:
        return Response({"trabajo_existe": False}, status=200)

    # Verificar si el trabajo está aprobado
    aprobado = TrabajoAprobado.objects.filter(id_trabajo=trabajo).exists()

    # Obtener versiones con acceso al objeto completo para usar .url y no conformidades
    versiones_qs = trabajo.versiones.all().order_by('-version_numero')
    versiones_data = []
    for v in versiones_qs:
        # Obtener no conformidades de esta versión
        no_conformidades = list(v.no_conformidades.values('id', 'no_conformidad'))
        versiones_data.append({
            'id': v.id,
            'version_numero': v.version_numero,
            'nombre_archivo': v.nombre_archivo,
            'tipo_archivo': v.tipo_archivo,
            'tamanio': v.tamanio,
            'descripcion': v.descripcion,
            'fecha_subida': v.fecha_subida.isoformat(),
            'archivo_url': v.archivo.url,
            'no_conformidades': no_conformidades,   
        })

    return Response({
        "trabajo_existe": True,
        "trabajo": {
            "id": trabajo.id,
            "titulo": trabajo.titulo,
            "tematica": trabajo.id_tematica.nombre,
            "aprobado": aprobado,                   
            "versiones": versiones_data
        }
    }, status=200)

@api_view(['POST'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def crear_version(request):
    try:
        participante = request.user.participante_profile
    except AttributeError:
        return Response({"error": "Solo participantes"}, status=403)

    trabajo_id = request.data.get('trabajo_id')
    archivo = request.FILES.get('archivo')
    descripcion = request.data.get('descripcion', '')

    if not trabajo_id or not archivo:
        return Response({"error": "Faltan campos"}, status=400)

    try:
        trabajo = Trabajo.objects.get(id=trabajo_id, id_participante=participante)
    except Trabajo.DoesNotExist:
        return Response({"error": "Trabajo no encontrado"}, status=404)

    ultima_version = trabajo.versiones.order_by('-version_numero').first()
    nueva_version_numero = (ultima_version.version_numero + 1) if ultima_version else 1

    extension = archivo.name.split('.')[-1].lower()
    if extension not in ['pdf', 'doc', 'docx']:
        return Response({"error": "Formato no permitido"}, status=400)

    nombre_base = os.path.splitext(archivo.name)[0]
    nombre_archivo = f"trabajo_{trabajo.id}_v{nueva_version_numero}_{nombre_base}.{extension}"
    carpeta_destino = f"trabajos/evento_{trabajo.evento.id}/trabajo_{trabajo.id}"
    ruta_completa = default_storage.save(os.path.join(carpeta_destino, nombre_archivo), ContentFile(archivo.read()))
    tamanio_kb = archivo.size // 1024

    version = VersionTrabajo.objects.create(
        trabajo=trabajo,
        version_numero=nueva_version_numero,
        archivo=ruta_completa,
        nombre_archivo=nombre_archivo,
        tipo_archivo=extension,
        tamanio=tamanio_kb,
        descripcion=descripcion
    )

    return Response({
        "mensaje": "Versión creada exitosamente",
        "version": version.version_numero,
        "archivo_url": version.archivo.url
    }, status=201)

@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def descargar_version(request, version_id):
    try:
        version = VersionTrabajo.objects.get(id=version_id)
        user = request.user
        
        # Verificar permisos
        if hasattr(user, 'oponente_profile'):
            # Oponente: solo si pertenece al mismo tribunal que el trabajo
            if version.trabajo.id_tribunal != user.oponente_profile.id_tribunal:
                return Response({"error": "No autorizado"}, status=403)
        elif hasattr(user, 'participante_profile'):
            # Participante: solo si es el dueño del trabajo
            if version.trabajo.id_participante.user != user:
                return Response({"error": "No autorizado"}, status=403)
        elif not user.is_staff:
            return Response({"error": "No autorizado"}, status=403)
        
        archivo = version.archivo
        if not archivo or not default_storage.exists(archivo.name):
            raise Http404
        
        response = FileResponse(default_storage.open(archivo.name, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{version.nombre_archivo}"'
        return response
    except VersionTrabajo.DoesNotExist:
        return Response({"error": "Versión no encontrada"}, status=404)