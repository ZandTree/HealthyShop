from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver

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


class Cart(models.Model):
    user     = models.OneToOneField(User,related_name='cart',on_delete=models.CASCADE)
    created  = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return "This is a cart of {}".format(self.user)

class CartItem(models.Model):
    product = models.ForeignKey(
                        Product,
                        related_name='items',
                        on_delete=models.CASCADE)

    cart    = models.ForeignKey(
                        Cart,
                        related_name='cart_items',
                        on_delete=models.CASCADE)

    qty     = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "Item is {}, amount is {} belongs to cart{}".format(
                self.product,
                self.qty,
                self.cart
                )



class Order(models.Model):
    cart     = models.OneToOneField(Cart,null=True,on_delete=models.SET_NULL)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return "This is an order {}, cart = {}".format(self.id)

@receiver(post_save,sender = User)
def create_user_cart(sender,instance,created,**kwargs):
    """As New User created, create Cart"""
    if created:
        Cart.objects.create(user=instance)
@receiver(post_save,sender=User)
def save_user_cart(sender,instance,**kwargs):
    """As New User created, save Cart"""
    instance.cart.save()
