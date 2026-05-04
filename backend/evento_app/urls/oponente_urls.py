from django.urls import path
from ..views.oponente_views import trabajos_tribunal, aprobar_trabajo, agregar_no_conformidad, obtener_no_conformidades, editar_no_conformidad, eliminar_no_conformidad

urlpatterns = [
 
    path('trabajos-tribunal/', trabajos_tribunal, name='trabajos_tribunal'),
    path('aprobar-trabajo/<int:trabajo_id>/', aprobar_trabajo, name='aprobar_trabajo'),
    path('agregar-no-conformidad/', agregar_no_conformidad, name='agregar_no_conformidad'),
    path('no-conformidades/<int:version_id>/', obtener_no_conformidades, name='obtener_no_conformidades'),
    path('editar-no-conformidad/<int:nc_id>/', editar_no_conformidad, name='editar_no_conformidad'),
path('eliminar-no-conformidad/<int:nc_id>/', eliminar_no_conformidad, name='eliminar_no_conformidad'),
]