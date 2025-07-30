
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from ..models import Post


@receiver(pre_save, sender=Post)
def delete_old_thumbnail_on_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)

            if old_instance.thumbnail and old_instance.thumbnail != instance.thumbnail:
                old_instance.thumbnail.delete(
                    save=False)

        except sender.DoesNotExist:
            pass


@receiver(post_delete, sender=Post)
def delete_thumbnail_on_delete(sender, instance, **kwargs):

    if instance.thumbnail:
        instance.thumbnail.delete(save=False)
