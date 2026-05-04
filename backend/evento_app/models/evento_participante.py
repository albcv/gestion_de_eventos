from django.db import models
from .evento import Evento
from .participante import Participante

class EventoParticipante(models.Model):
    id_evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    id_participante = models.ForeignKey(Participante, on_delete=models.CASCADE)

    class Meta:
        unique_together = [["id_evento", "id_participante"]]

    def __str__(self):
        return f"{self.id_evento.nombre} - {self.id_participante.user.username}"