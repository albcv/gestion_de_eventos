from django.contrib import admin
from evento_app.models import EventoTematica

@admin.register(EventoTematica)
class EventoTematicaAdmin(admin.ModelAdmin):
    list_display = ('id_evento', 'id_tematica')
    autocomplete_fields = ('id_evento', 'id_tematica')
