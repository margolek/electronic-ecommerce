from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Product, Images
from ecommerce.settings import PRODUCT_DEFAULT_IMAGE_NAME


@receiver(post_save, sender=Product)
def save_default_photo(sender, instance, **kwargs):

    exist = Images.objects.filter(product_id=instance.id).exists()

    if not exist:
        Images.objects.create(product_id=instance.id, default=True)


@receiver(post_save, sender=Images)
def get_image(sender, instance, **kwargs):

    if instance.image.name != PRODUCT_DEFAULT_IMAGE_NAME:
        Images.objects.filter(image=PRODUCT_DEFAULT_IMAGE_NAME).filter(
            product_id=instance.product.pk).delete()
        query = Images.objects.filter(product_id=instance.product.pk)
        if len(query) == 1:
            Images.objects.filter(image=instance.image.name).filter(
                product_id=instance.product.pk).update(default=True)


# @receiver(post_delete, sender=Images)
# def get_default_image(sender, instance, **kwargs):
#     empty = Images.objects.filter(product_id=instance.product.pk)
#     if len(empty) == 0:
#         Images.objects.create(product_id=instance.product.pk, default=True)
