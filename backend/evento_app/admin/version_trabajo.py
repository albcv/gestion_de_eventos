from django.contrib import admin
from evento_app.models import VersionTrabajo

@admin.register(VersionTrabajo)
class VersionTrabajoAdmin(admin.ModelAdmin):
    list_display = ('id', 'trabajo', 'version_numero', 'nombre_archivo', 'tipo_archivo', 'tamanio', 'fecha_subida')
    search_fields = ('trabajo__titulo', 'nombre_archivo')
    list_filter = ('tipo_archivo', 'fecha_subida')
    autocomplete_fields = ('trabajo',)  
    readonly_fields = ('fecha_subida',)

   
