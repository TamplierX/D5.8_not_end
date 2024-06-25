from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post


@receiver(post_save, sender=Post)
def product_created(instance, **kwargs):
    print('Создан пост', instance)
