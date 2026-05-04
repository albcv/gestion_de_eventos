from django.db import models

class Provincia(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre de la provincia (único)"
    )

    def __str__(self):
        return self.nombre