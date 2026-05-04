from django.db import models
from .provincia import Provincia

class Municipio(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre del municipio (único)"
    )
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.PROTECT,
        related_name="municipios"
    )

    def __str__(self):
        return f"{self.nombre} ({self.provincia.nombre})"