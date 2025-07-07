from django.db import models
from django.contrib.auth.models import User
import os
from .utils import logo_upload_path
from PIL import Image

class Identity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='identity')
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to=logo_upload_path, default="tenant_logos/default_logo.jpg")
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        old_logo_path = None

        # Obtener logo anterior si existe
        if self.pk:  
            try:
                old = Identity.objects.get(pk=self.pk)
                if old.logo and old.logo != self.logo:
                    old_logo_path = old.logo.path
            except Identity.DoesNotExist:
                pass

        # Guardar primero el nuevo logo
        super().save(*args, **kwargs)

        # Eliminar el archivo anterior si cambió
        if old_logo_path and os.path.isfile(old_logo_path) and old_logo_path != "/app/media/tenant_logos/default_logo.jpg":
            os.remove(old_logo_path)

        # Redimensionar el logo nuevo si existe
        if self.logo:
            try:
                img = Image.open(self.logo.path)
                if img.height > 600 or img.width > 600:
                    img.thumbnail((600, 600))
                    img.save(self.logo.path)
            except Exception as e:
                print(f"Error resizing logo: {e}")