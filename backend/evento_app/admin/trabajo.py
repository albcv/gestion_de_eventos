from django.contrib import admin
from evento_app.models import Trabajo, VersionTrabajo

class VersionTrabajoInline(admin.TabularInline):  
    model = VersionTrabajo
    extra = 1 
    fields = ('version_numero', 'archivo', 'nombre_archivo', 'tipo_archivo', 'tamanio', 'descripcion', 'fecha_subida')
    readonly_fields = ('fecha_subida',)  
   
    ordering = ('-version_numero',)

@admin.register(Trabajo)
class TrabajoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'id_participante', 'id_tematica', 'id_tribunal')
    search_fields = ('titulo',)
    list_filter = ('id_tematica', 'id_participante')
    autocomplete_fields = ('id_participante', 'id_tematica', 'id_tribunal')
    inlines = [VersionTrabajoInline]   