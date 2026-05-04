from django.contrib import admin
from evento_app.models import Tematica, EventoTematica

class EventoTematicaInline(admin.TabularInline):
    model = EventoTematica
    extra = 1
   
   

@admin.register(Tematica)
class TematicaAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)
    list_display = ('nombre',)
    inlines = [EventoTematicaInline]