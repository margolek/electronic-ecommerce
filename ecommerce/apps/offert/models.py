from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Category(MPTTModel):
    """
    MPTT Model allow us simple access to hierarchical data
    """

    name = models.CharField(verbose_name=_(
        "Group Name"), max_length=255, unique=True)
    photo = models.ImageField(upload_to="category/",
                              default="category/default_photo.png")
    slug = models.SlugField(verbose_name=_(
        "Group Slug"), max_length=255, unique=True)
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

    name = models.CharField(verbose_name=_(
        "Feature Name"), max_length=255, unique=True)
    category = models.ManyToManyField(
        Category, related_name="feature_categories", through="FeatureCategory"
    )

    def __str__(self):
        return f"{self.name}"


class FeatureCategory(models.Model):
    """
    Connection between Feature and Category
    """

    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["feature", "category"]

    def __str__(self):
        return f"{self.feature} : {self.category}"


class Product(models.Model):
    """
    Contain product items
    """

    name = models.CharField(verbose_name=_(
        "Product Name"), max_length=255, unique=True)
    slug = models.SlugField(verbose_name=_(
        "Slug"), max_length=255, unique=True)
    category = TreeForeignKey(Category, on_delete=models.PROTECT)
    features = models.ManyToManyField(
        Feature, related_name="features", through="ProductFeature"
    )
    description = models.TextField(
        verbose_name=_("Product Description"), blank=True)
    added_by = models.ForeignKey(
        User, related_name="product_creator", on_delete=models.CASCADE
    )
    added_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_modification = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    quantity = models.DecimalField(max_digits=5, decimal_places=0)
    calatog_number = models.DecimalField(max_digits=10, decimal_places=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductRate(models.Model):
    """
    All users opinion about product
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=2, decimal_places=1)


class ProductFeature(models.Model):
    """
    ManytoMany Relationship connector
    """

    product = models.ForeignKey(
        Product, related_name="product_product", on_delete=models.CASCADE
    )
    feature = models.ForeignKey(
        Feature, related_name="product_feature", on_delete=models.CASCADE
    )
    value = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name=_("Feature Value"),
        help_text="max 6 digit, 2 decimal place",
    )

    class Meta:
        unique_together = ["product", "feature"]

    def __str__(self):
        return f"{self.product} : {self.feature}"


class Images(models.Model):
    """
    Product images details
    """

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
    """
    Product price details
    """

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
