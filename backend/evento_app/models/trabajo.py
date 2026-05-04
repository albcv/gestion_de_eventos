from django.db import models
from .participante import Participante
from .tematica import Tematica
from .tribunal import Tribunal
from .evento import Evento

class Trabajo(models.Model):
    titulo = models.CharField(
        max_length=300,
        unique=True,
        help_text="Título del trabajo (único)"
    )
    id_participante = models.OneToOneField(
        Participante,  
        on_delete=models.CASCADE,
        related_name="trabajo",
        help_text="Participante autor (único por trabajo)"
    )
    id_tematica = models.ForeignKey(
        Tematica,
        on_delete=models.PROTECT,
        related_name="trabajos",
        help_text="Temática asociada"
    )
    id_tribunal = models.ForeignKey(
        Tribunal,
        on_delete=models.PROTECT,
        related_name="trabajos",
        help_text="Tribunal encargado de revisar el trabajo"
    )

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='trabajos')

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo