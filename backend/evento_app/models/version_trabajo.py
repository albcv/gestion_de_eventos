from django.db import models
from .trabajo import Trabajo

class VersionTrabajo(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, related_name='versiones')
    version_numero = models.PositiveIntegerField()
    archivo = models.FileField(upload_to='trabajos/%Y/%m/%d/')  
    nombre_archivo = models.CharField(max_length=255)
    tipo_archivo = models.CharField(max_length=10)  # pdf, doc, docx
    tamanio = models.PositiveIntegerField(verbose_name="Tamaño (KB)")
    descripcion = models.TextField(blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trabajo', 'version_numero')
        ordering = ['-version_numero']
        verbose_name = "Versión de trabajo"
        verbose_name_plural = "Versiones de trabajo"

    def delete(self, *args, **kwargs):
        # Eliminar archivo físico antes de borrar el registro
        if self.archivo:
            storage, path = self.archivo.storage, self.archivo.path
            storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.trabajo.titulo} v{self.version_numero}"