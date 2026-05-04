from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .municipio import Municipio

class Entidad(models.Model):
    nombre = models.CharField(
        max_length=200,
        unique=True,
        help_text="Nombre completo de la entidad patrocinadora"
    )
    siglas = models.CharField(
        max_length=20,
        unique=True,
        help_text="Siglas de la entidad (máx. 20 caracteres)"
    )
    
    id_municipio = models.ForeignKey(
        Municipio,
        on_delete=models.PROTECT,
        related_name="entidades",
        help_text="Municipio donde se ubica la entidad"
    )
    direccion = models.CharField(
        max_length=255,
        unique=True,
        help_text="Dirección completa (única por entidad)"
    )

    class Meta:
        verbose_name = "Entidad"
        verbose_name_plural = "Entidades"

    def __str__(self):
        return f"{self.nombre} ({self.siglas})"