from django.db import models
from django.urls import reverse
from djmoney.models.fields import MoneyField
# Create your models here.

"""
Product models for the catalog

SOLID principle design pattern

Each model handles 1 responsibility
TimeStampModel can be extended
Models depend on Abstractions

"""

# Abstract Base Model
class TimeStampedModel(models.Model):
    # field shoud not be editable and set only once
    created_at = models.DateTimeField(auto_now_add=True)
    # field should be updated during update
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    # anything that needs longer should use TextField - but usually 255
    name = models.CharField(max_length=255, unique=True)
    # usually not too long, affects SEO. blank is true, generate at a later time via signals
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    # description will be set with no max length for now, can be communicated internally with product team
    description = models.TextField(blank=True)

    class Meta:
        # house keeping in django admin
        verbose_name_plural = "categories"
        # order by name, convention
        ordering = ["name"]
    
    # more admin creature comforts
    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("products:product_list") + f"?category={self.pk}"
    
# Each product should have a tag 
class Tag(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        ordering = ["name"]
    
    def __str__(self) -> str:
        return self.name
    
# Currency model 
# Can be stored as Canadian or US during creation, and convert based on user location
class Currency(models.TextChoices):
    CAD = "CAD", "Canadian Dollar"
    USD = "USD", "US Dollar"

# Main model  
class Product(TimeStampedModel):
    # omitted unique at this level, differentiated at tag, category level
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    # using Moneyfield here for Dependency Inversion, can use "convert_money" function
    price = MoneyField(max_digits=14, decimal_places=2, currency_choices=Currency.choices)
    # Many products under 1 category
    category = models.ForeignKey(
        Category,
        # usually I do cascade delete, but that's for user data(right to be forgotten),
        # but products should be saved in case naming changes due to rebranding
        on_delete=models.PROTECT,
        related_name="products",
    )
    # products can have multiple tags
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="products",
    )
    # just in case we want to hide products
    is_active = models.BooleanField(default=True)

    class Meta:
        # descending order
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return self.name
