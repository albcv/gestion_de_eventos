from django.contrib import admin
from evento_app.models import Tribunal

@admin.register(Tribunal)
class TribunalAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
