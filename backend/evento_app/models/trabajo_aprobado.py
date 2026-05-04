# models.py
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
    documento = models.FileField(
        upload_to='presentaciones/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="Archivo PowerPoint del trabajo aprobado",
        verbose_name="Power Point",
    )

    class Meta:
        verbose_name = "Trabajo aprobado"
        verbose_name_plural = "Trabajos aprobados"

    def __str__(self):
        return f"Aprobado: {self.id_trabajo.titulo}"