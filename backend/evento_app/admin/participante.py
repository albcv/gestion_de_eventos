from django.contrib import admin
from evento_app.models import Participante

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido1', 'apellido2', 'user')
    search_fields = ('nombre', 'apellido1', 'apellido2')
    list_filter = ('nombre', 'apellido1', 'apellido2')
    autocomplete_fields = ('user',)
