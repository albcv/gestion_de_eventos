from django.contrib import admin
from evento_app.models import EventoParticipante

@admin.register(EventoParticipante)
class EventoParticipanteAdmin(admin.ModelAdmin):
    list_display = ('id_evento', 'id_participante')
    autocomplete_fields = ('id_evento', 'id_participante')
