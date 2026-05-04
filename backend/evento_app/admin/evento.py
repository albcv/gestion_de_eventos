from django.contrib import admin
from evento_app.models import Evento, EventoTematica, Tematica

class EventoTematicaInline(admin.TabularInline):  
    model = EventoTematica
    extra = 1
   

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_apertura', 'fecha_cierre', 'id_entidad')
    search_fields = ('nombre',)
    list_filter = ('fecha_apertura', 'fecha_cierre')
    autocomplete_fields = ('id_entidad',)
    inlines = [EventoTematicaInline]   