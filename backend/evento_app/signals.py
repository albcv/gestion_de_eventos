import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import VersionTrabajo

@receiver(post_delete, sender=VersionTrabajo)
def eliminar_archivo_version(sender, instance, **kwargs):
    if instance.archivo and os.path.isfile(instance.archivo.path):
        os.remove(instance.archivo.path)