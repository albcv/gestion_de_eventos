from django.contrib import admin
from evento_app.models import NoConformidad

@admin.register(NoConformidad)
class NoConformidadAdmin(admin.ModelAdmin):
    list_display = ('id_version_trabajo', 'no_conformidad')
    autocomplete_fields = ('id_version_trabajo',)
