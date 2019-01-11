from django.db import models
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    """Categories of the products"""
    name = models.CharField(max_length=50,unique=True)
    parent = TreeForeignKey(
        'self',
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        related_name = 'children'
    )
    slug = models.SlugField(max_length=100,unique=True)

    class MPTTMeta:
        order_insersion_by = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(
                    Category,
                    related_name='products',
                    on_delete=models.CASCADE
                    )
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    description = models.TextField()
    price = models.IntegerField(default=0)
    availability = models.BooleanField(default=True)
    quantity = models.IntegerField(default = 1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

    class Meta:
        verbose_name_plural = 'Products'
