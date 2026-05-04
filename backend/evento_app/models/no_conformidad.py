from django.db import models
from .version_trabajo import VersionTrabajo

class NoConformidad(models.Model):
    id_version_trabajo = models.ForeignKey(   
        VersionTrabajo,
        on_delete=models.CASCADE,
        related_name="no_conformidades",
        help_text="Versión del trabajo que presenta no conformidad"
    )
    no_conformidad = models.TextField(
        help_text="Descripción de la no conformidad"
    )

    class Meta:
        verbose_name = "No conformidad"
        verbose_name_plural = "No conformidades"

    def __str__(self):
        return f"No conformidad para {self.id_version_trabajo}"