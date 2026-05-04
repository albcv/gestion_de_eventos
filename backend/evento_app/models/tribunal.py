from django.db import models

class Tribunal(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        help_text="Identificador o nombre del tribunal"
    )
    class Meta:
        verbose_name = "Tribunal"
        verbose_name_plural = "Tribunales"
    
    def __str__(self):
        return self.nombre