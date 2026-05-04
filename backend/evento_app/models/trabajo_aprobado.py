from django.db import models
from .trabajo import Trabajo

class TrabajoAprobado(models.Model):
    id_trabajo = models.OneToOneField(
        Trabajo,
        on_delete=models.CASCADE,
        related_name="aprobacion",
        help_text="Trabajo aprobado (relación uno a uno)"
    )
    pago = models.BooleanField(
        default=False,
        help_text="Indica si el pago fue realizado"
    )
    ruta_documento = models.CharField(
        max_length=500,
        unique=True,
        help_text="Ruta del archivo PowerPoint de la presentación aprobada"
    )

    class Meta:
        verbose_name = "Trabajo aprobado"
        verbose_name_plural = "Trabajos aprobados"

    def __str__(self):
        return f"Aprobado: {self.id_trabajo.titulo}"