from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    MPTT Model allow us simple access to hierarchical data
    """

    name = models.CharField(verbose_name=_("Group Name"), max_length=255, unique=True)
    slug = models.SlugField(verbose_name=_("Group Slug"), max_length=255, unique=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Feature(models.Model):
    """
    Contain certain product specification with define value
    """

    name = models.CharField(verbose_name=_("Feature Name"), max_length=255, unique=True)
    value = models.DecimalField(
        verbose_name=_("Feature value"), max_digits=6, decimal_places=2
    )

    def __str__(self):
        return f"{self.name} : {self.value}"


class Product(models.Model):
    """
    Contain product items
    """

    name = models.CharField(verbose_name=_("Product Name"), max_length=255, unique=True)
    slug = models.SlugField(verbose_name=_("Slug"), max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Images(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_image"
    )
    default = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to="images/", verbose_name=_("image"), default="images/default_photo.jpg"
    )

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")


class Price(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    regular = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Normal Price"
    )
    day_product_price = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Day Product Price"
    )
    day_product = models.BooleanField(default=False)
    in_sale_price = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Sale Price"
    )
    in_sale = models.BooleanField(default=False)
