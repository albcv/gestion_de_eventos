from django.conf import settings
from django.core.files.storage import default_storage
from django.http import FileResponse
from ..authentication import CookieTokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Trabajo, TrabajoAprobado, NoConformidad, VersionTrabajo 

@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def trabajos_tribunal(request):
    try:
        oponente = request.user.oponente_profile
    except AttributeError:
        return Response({"error": "Solo oponentes"}, status=403)

    tribunal = oponente.id_tribunal
    trabajos = Trabajo.objects.filter(id_tribunal=tribunal).select_related(
        'id_participante', 'id_tematica', 'evento'
    ).prefetch_related('versiones', 'aprobacion')

    data = []
    for trabajo in trabajos:
        aprobado_obj = getattr(trabajo, 'aprobacion', None)
        aprobado = aprobado_obj is not None
        powerpoint = None
        if aprobado_obj and aprobado_obj.documento:
            # Si documento es FileField
            if hasattr(aprobado_obj.documento, 'url'):
                powerpoint = {
                    "url": aprobado_obj.documento.url,
                    "nombre_archivo": aprobado_obj.documento.name.split('/')[-1]
                }
            else:
                # Si es CharField con ruta
                powerpoint = {
                    "url": f"{settings.MEDIA_URL}{aprobado_obj.documento}",
                    "nombre_archivo": aprobado_obj.documento.split('/')[-1]
                }

        versiones_data = []
        for v in trabajo.versiones.all().order_by('-version_numero'):
            versiones_data.append({
                'id': v.id,
                'version_numero': v.version_numero,
                'nombre_archivo': v.nombre_archivo,
                'tipo_archivo': v.tipo_archivo,
                'tamanio': v.tamanio,
                'descripcion': v.descripcion,
                'fecha_subida': v.fecha_subida.isoformat(),
            })

        data.append({
            'id': trabajo.id,
            'titulo': trabajo.titulo,
            'participante': f"{trabajo.id_participante.nombre} {trabajo.id_participante.apellido1}",
            'tematica': trabajo.id_tematica.nombre,
            'evento': trabajo.evento.nombre,
            'aprobado': aprobado,
            'powerpoint': powerpoint,
            'versiones': versiones_data
        })

    return Response(data, status=200)



@api_view(['POST'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def aprobar_trabajo(request, trabajo_id):
    """Marca un trabajo como aprobado (lo inserta en TrabajoAprobado)."""
    try:
        oponente = request.user.oponente_profile
    except AttributeError:
        return Response({"error": "Solo oponentes pueden aprobar trabajos"}, status=403)
    
    try:
        trabajo = Trabajo.objects.get(id=trabajo_id)
    except Trabajo.DoesNotExist:
        return Response({"error": "Trabajo no encontrado"}, status=404)
    
    # Verificar que el oponente pertenezca al tribunal del trabajo
    if trabajo.id_tribunal != oponente.id_tribunal:
        return Response({"error": "No autorizado para este trabajo"}, status=403)
    
    # Verificar si ya está aprobado
    if TrabajoAprobado.objects.filter(id_trabajo=trabajo).exists():
        return Response({"error": "El trabajo ya está aprobado"}, status=400)
    
    # Crear el registro de trabajo aprobado
    aprobado = TrabajoAprobado.objects.create(
        id_trabajo=trabajo,
        pago=False,   # por defecto; se puede actualizar después
        documento=''  # opcional, podría ser la última versión
        # Si quieres guardar la ruta del documento de la última versión:
        # ultima_version = trabajo.versiones.order_by('-version_numero').first()
        # if ultima_version: aprobado.documento = ultima_version.archivo.name
    )
    return Response({"message": "Trabajo aprobado correctamente", "aprobado_id": aprobado.id}, status=201)

@api_view(['POST'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def agregar_no_conformidad(request):
    """Agrega una no conformidad a una versión de un trabajo."""
    try:
        oponente = request.user.oponente_profile
    except AttributeError:
        return Response({"error": "Solo oponentes pueden agregar no conformidades"}, status=403)
    
    version_id = request.data.get('version_id')
    texto = request.data.get('texto', '').strip()
    
    if not version_id or not texto:
        return Response({"error": "Faltan campos (version_id, texto)"}, status=400)
    
    try:
        version = VersionTrabajo.objects.get(id=version_id)
    except VersionTrabajo.DoesNotExist:
        return Response({"error": "Versión no encontrada"}, status=404)
    
    # Verificar que el oponente pertenezca al tribunal del trabajo
    if version.trabajo.id_tribunal != oponente.id_tribunal:
        return Response({"error": "No autorizado para esta versión"}, status=403)
    
    # Crear la no conformidad
    nc = NoConformidad.objects.create(
        id_version_trabajo=version,
        no_conformidad=texto
    )
    return Response({
        "message": "No conformidad agregada",
        "id": nc.id,
        "no_conformidad": nc.no_conformidad
    }, status=201)

@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def obtener_no_conformidades(request, version_id):
    try:
        version = VersionTrabajo.objects.get(id=version_id)
    except VersionTrabajo.DoesNotExist:
        return Response({"error": "Versión no encontrada"}, status=404)
    
    # Verificar permisos
    user = request.user
    if hasattr(user, 'oponente_profile'):
        if version.trabajo.id_tribunal != user.oponente_profile.id_tribunal:
            return Response({"error": "No autorizado"}, status=403)
    elif not user.is_staff:
        return Response({"error": "No autorizado"}, status=403)
    
    # Obtener no conformidades mediante el modelo NoConformidad
    from ..models import NoConformidad  # Importar al inicio del archivo
    no_conformidades = NoConformidad.objects.filter(id_version_trabajo=version).values('id', 'no_conformidad', 'id_version_trabajo')
    return Response(list(no_conformidades), status=200)


@api_view(['PUT'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def editar_no_conformidad(request, nc_id):
    try:
        oponente = request.user.oponente_profile
    except AttributeError:
        return Response({"error": "Solo oponentes"}, status=403)
    
    try:
        nc = NoConformidad.objects.get(id=nc_id)
    except NoConformidad.DoesNotExist:
        return Response({"error": "No conformidad no encontrada"}, status=404)
    
    # Verificar que el oponente pertenezca al tribunal del trabajo
    trabajo = nc.id_version_trabajo.trabajo
    if trabajo.id_tribunal != oponente.id_tribunal:
        return Response({"error": "No autorizado"}, status=403)
    
    nuevo_texto = request.data.get('texto', '').strip()
    if not nuevo_texto:
        return Response({"error": "El texto no puede estar vacío"}, status=400)
    
    nc.no_conformidad = nuevo_texto
    nc.save()
    return Response({
        "id": nc.id,
        "no_conformidad": nc.no_conformidad,
        "id_version_trabajo": nc.id_version_trabajo.id
    }, status=200)

@api_view(['DELETE'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def eliminar_no_conformidad(request, nc_id):
    try:
        oponente = request.user.oponente_profile
    except AttributeError:
        return Response({"error": "Solo oponentes"}, status=403)
    
    try:
        nc = NoConformidad.objects.get(id=nc_id)
    except NoConformidad.DoesNotExist:
        return Response({"error": "No conformidad no encontrada"}, status=404)
    
    trabajo = nc.id_version_trabajo.trabajo
    if trabajo.id_tribunal != oponente.id_tribunal:
        return Response({"error": "No autorizado"}, status=403)
    
    nc.delete()
    return Response({"message": "No conformidad eliminada"}, status=200)


@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def descargar_powerpoint_tribunal(request, trabajo_id):
    try:
        oponente = request.user.oponente_profile
    except AttributeError:
        return Response({"error": "Solo oponentes"}, status=403)

    try:
        trabajo = Trabajo.objects.get(id=trabajo_id)
    except Trabajo.DoesNotExist:
        return Response({"error": "Trabajo no encontrado"}, status=404)

    # Verificar que el trabajo pertenezca al tribunal del oponente
    if trabajo.id_tribunal != oponente.id_tribunal:
        return Response({"error": "No autorizado"}, status=403)

    aprobado = getattr(trabajo, 'aprobacion', None)
    if not aprobado or not aprobado.documento:
        return Response({"error": "No hay PowerPoint disponible"}, status=404)

    archivo = aprobado.documento
    if not default_storage.exists(archivo.name):
        return Response({"error": "Archivo no encontrado"}, status=404)

    response = FileResponse(default_storage.open(archivo.name, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{archivo.name.split("/")[-1]}"'
    return response