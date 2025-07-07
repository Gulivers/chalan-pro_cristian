from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Identity

@receiver(post_save, sender=User)
def create_empresa(sender, instance, created, **kwargs):
    if created:
        Identity.objects.create(user=instance)