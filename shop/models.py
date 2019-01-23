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

# class ImageGroup(models.Model):
#     """ Дорабатываю   Upload images in admin,list,detail view"""
#     product = models.ForeignKey(Product,related_name='images',on_delete=models.CASCADE)
#     images = models.ImageField(null=True,blank=True,upload_to=img_list)

    # def save(self,*args,**kwargs):
    #     super().save(*args,**kwargs)
    #     if self.images:
    #         img = Image.open(self.images.apth)
    #         #....check for sizes
    #         images.save()
    #
    # def __str__(self):
    #     return 'img {}'.format(self.id)
    # @property
    # def get_images_url(self):
    #    путь к папке с картинками
    #     if self.images:
    #         return '/media/{}'.format(self.images)
    #     else:
    #         если картинки нет, то показать дефолт
    #         return 'static/img/default.jpg'


class Cart(models.Model):
    user = models.ForeignKey(User,related_name='cart',on_delete=models.CASCADE)
    created  = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return "This is a cart of {}".format(self.user)

class CartItem(models.Model):
    product = models.ForeignKey(
                        Product,
                        related_name='items',
                        on_delete=models.CASCADE)

    cart = models.ForeignKey(
                        Cart,
                        related_name='cart_items',
                        on_delete=models.CASCADE)

    qty = models.PositiveIntegerField(default=0)
    subtotal_price = models.PositiveIntegerField(default=0,editable=False)

    def __str__(self):
        return "Item is {}, amount is {} belongs to cart{}".format(
                self.product,
                self.qty,
                self.cart
                )
    def save(self,*args,**kwargs):
        """ generate price for each product item(price 1st*quantity)"""
        self.subtotal_price = self.qty * self.product.price
        super().save(*args,**kwargs)



class Order(models.Model):
    cart = models.ForeignKey(Cart,related_name='order',on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return "This is an order {}".format(self.id)


@receiver(post_save,sender = User)
def create_user_cart(sender,instance,created,**kwargs):
    """If New User created, create Cart"""
    if created:
        # let op: id card will be change (ForeignKey)
        Cart.objects.create(user=instance)


# draft from StackOverFlow
# @receiver(post_save, sender=CartItem)
# def update_cart(sender, instance, **kwargs):
#     subtotal = instance.qty * instance.product.price
#     instance.cart.total += subtotal
#     instance.cart.count += instance.quantity
#     instance.cart.updated = datetime.now()
