from django.urls import path
from ..views.participante_views import crear_trabajo, obtener_mi_trabajo, crear_version, descargar_version, subir_powerpoint, descargar_powerpoint

urlpatterns = [
 
    path('trabajos/crear/', crear_trabajo, name='crear_trabajo'),
    path('mi-trabajo/', obtener_mi_trabajo, name='mi_trabajo'),
    path('crear-version/', crear_version, name='crear_version'),
    path('descargar-version/<int:version_id>/', descargar_version, name='descargar_version'),
    path('subir-powerpoint/', subir_powerpoint, name='subir_powerpoint'),
    path('descargar-powerpoint/', descargar_powerpoint, name='descargar_powerpoint'),
]