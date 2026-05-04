from django.contrib import admin
from evento_app.models import Oponente

@admin.register(Oponente)
class OponenteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido1', 'apellido2', 'user', 'id_tribunal')
    search_fields = ('nombre', 'apellido1', 'apellido2')
    list_filter = ('id_tribunal', 'nombre', 'apellido1', 'apellido2')
    autocomplete_fields = ('user', 'id_tribunal')
