from django.db import models
from django.contrib.auth.models import User
from .persona_base import PersonaBase


class Participante(PersonaBase):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="participante_profile"
    )

    grado_cientifico=models.CharField(
        max_length=50,
    )

    def __str__(self):
        return f"{self.nombre_completo()})"