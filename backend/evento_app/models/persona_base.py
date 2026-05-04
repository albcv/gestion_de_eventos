from django.db import models


class PersonaBase(models.Model):
    nombre = models.CharField(
        max_length=100,
        help_text="Nombre(s)"
    )
    apellido1 = models.CharField(
        max_length=100,
        help_text="Primer apellido"
    )
    apellido2 = models.CharField(
        max_length=100,
        blank=True,
        help_text="Segundo apellido"
    )
   
    class Meta:
        abstract = True

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido1} {self.apellido2}".strip()