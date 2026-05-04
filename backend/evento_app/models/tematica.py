from django.db import models

class Tematica(models.Model):
    nombre = models.CharField(
        max_length=150,
        unique=True,
        help_text="Nombre de la temática (único)"
    )

    class Meta:
        verbose_name = "Temática"
        verbose_name_plural = "Temáticas"


    def __str__(self):
        return self.nombre