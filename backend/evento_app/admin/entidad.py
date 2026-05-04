from django.contrib import admin
from evento_app.models import Entidad

@admin.register(Entidad)
class EntidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'siglas', 'id_municipio', 'direccion')
    search_fields = ('nombre', 'siglas',)
    autocomplete_fields = ('id_municipio',)
