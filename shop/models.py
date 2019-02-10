from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from photologue.models import Gallery
from django.utils import timezone

class Star(models.Model):
    """
    represent a scale of 5 stars :
    user can choose between s5 = max score 5, s1 = min score 1
    """
    count_s5 = models.PositiveIntegerField(default=0)
    count_s4 = models.PositiveIntegerField(default=0)
    count_s3 = models.PositiveIntegerField(default=0)
    count_s2 = models.PositiveIntegerField(default=0)
    count_s1 = models.PositiveIntegerField(default=0)
    result = models.DecimalField(max_digits=2,decimal_places=1)
    user = models.ForeignKey(User,
                    related_name='user_stars',
                    null=True,
                    blank=True,
                    on_delete=models.CASCADE
                    )
    def __str__(self):
        return "current rating is {}".format(self.result)

    def save(self,*args,**kwargs):
        """
        get amount of votes for each star in range(5)
        return avarage of stars value
        """
        stars = self.count_s5 + self.count_s4 + self.count_s3 + self.count_s2 + self.count_s1
        if stars == 0:
            stars = 1
        sum_stars = (5*self.count_s5+4*self.count_s4+3*self.count_s3+2*self.count_s2+1*self.count_s1)/stars
        self.result = round(sum_stars,1)
        super().save(*args,**kwargs)

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

    class Meta:
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
    gallery = models.ForeignKey(Gallery,on_delete=models.SET_NULL,null=True,blank=True)
    sale = models.BooleanField(default=False)
    rating = models.OneToOneField(Star,
                        blank=True,
                        null=True,
                        related_name='prod_rating',
                        on_delete =models.SET_NULL
                        )
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_comments')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) #s,default=timezone.now)
    changed_ad = models.DateTimeField(auto_now=True) #,default=timezone.now)

    def __str__(self):
        return "comment of {}".format(self.comment)

class CreateCartManager(models.Manager):
    def new_cart(self,user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)
class Cart(models.Model):
    #user = models.ForeignKey(User,related_name='cart',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='cart',null=True,blank=True,on_delete=models.SET_NULL)
    accepted = models.BooleanField(default=False)
    created  = models.DateTimeField(auto_now_add=True)
    #updated = models.DateTimeField(auto_now=True)
    objects = CreateCartManager()

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

# ORDER_STATUS_CHOICES = (
#     #('db','to display')
#     ('created','Created'),
#     ('paid','Paid'),
#     ('shipped','Shipped'),
#     ('refunded','Refunded')
# )
class Order(models.Model):
    #order_ident = models.CharField(max_length=120,blank=True) #AB3245
    shipping_total = models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    total = models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    cart = models.ForeignKey(Cart,related_name='order',on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True )

    def __str__(self):
        return "This is an order {}".format(self.id)

@receiver(post_save,sender=Product)
def create_rating(sender,instance,created,**kwargs):
    if created:
        Product.objects.filter(id=instance.id).update(rating=instance.id)
        Star.objects.create(id=instance.id)


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
