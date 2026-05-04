from django.db import models
from .evento import Evento
from .tematica import Tematica

class EventoTematica(models.Model):
    id_evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    id_tematica = models.ForeignKey(Tematica, on_delete=models.CASCADE)

    class Meta:
        unique_together = [["id_evento", "id_tematica"]]
        verbose_name = "Evento temática"
        verbose_name_plural = "Evento temáticas"

    def __str__(self):
        return f"{self.id_evento.nombre} - {self.id_tematica.nombre}"