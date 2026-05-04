from django.urls import path
from ..views.participante_views import crear_trabajo, obtener_mi_trabajo, crear_version, descargar_version

urlpatterns = [
 
    path('trabajos/crear/', crear_trabajo, name='crear_trabajo'),
    path('mi-trabajo/', obtener_mi_trabajo, name='mi_trabajo'),
    path('crear-version/', crear_version, name='crear_version'),
    path('descargar-version/<int:version_id>/', descargar_version, name='descargar_version'),
]