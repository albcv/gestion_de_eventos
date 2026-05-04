from django.db import models
from django.contrib.auth.models import User
from .tribunal import Tribunal
from .persona_base import PersonaBase

class Oponente(PersonaBase):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="oponente_profile"
    )
    id_tribunal = models.ForeignKey(
        Tribunal,
        on_delete=models.PROTECT,
        related_name="oponentes",
        help_text="Tribunal al que pertenece el oponente"
    )

    def __str__(self):
        return f"{self.nombre_completo()} - {self.id_tribunal.nombre}"