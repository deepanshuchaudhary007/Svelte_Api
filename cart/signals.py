from users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cart


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        print("signals saved.......................")
        Cart.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_cart(sender, instance, **kwargs):
#     print("signals saved.......................")
#     instance.user.save()