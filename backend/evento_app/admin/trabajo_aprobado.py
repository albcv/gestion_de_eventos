from django.contrib import admin
from evento_app.models import TrabajoAprobado

@admin.register(TrabajoAprobado)
class TrabajoAprobadoAdmin(admin.ModelAdmin):
    list_display = ('id_trabajo', 'pago', 'documento')
    autocomplete_fields = ('id_trabajo',)
