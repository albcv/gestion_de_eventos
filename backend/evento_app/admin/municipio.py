from django.contrib import admin
from evento_app.models import Municipio

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'provincia')
    search_fields = ('nombre', 'provincia__nombre')
    autocomplete_fields = ('provincia',)
