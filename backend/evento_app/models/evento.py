from django.db import models
from .entidad import Entidad

class Evento(models.Model):
    nombre = models.CharField(
        max_length=200,
        unique=True,
        help_text="Nombre del evento (único)"
    )
    fecha_apertura = models.DateTimeField()
    fecha_cierre = models.DateTimeField()
    id_entidad = models.ForeignKey(
        Entidad,
        on_delete=models.PROTECT,
        related_name="eventos",
        help_text="Entidad que patrocina el evento"
    )
    # Relaciones ManyToMany definidas mediante tablas explícitas
    tematicas = models.ManyToManyField(
        "Tematica",
        through="EventoTematica",
        related_name="eventos"
    )
    participantes = models.ManyToManyField(
        "Participante",
        through="EventoParticipante",
        related_name="eventos"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(fecha_cierre__gt=models.F("fecha_apertura")),
                name="fecha_cierre_posterior_a_apertura"
            )
        ]

    def __str__(self):
        return self.nombre