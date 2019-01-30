from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

COUNTRY_CHOICES = (
    ('USA','USA'),
    ('Gabon','Gabon'),
    ('VK','England'),
    ('Japan','Japan')
)

class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    country = models.CharField(max_length=120,choices=COUNTRY_CHOICES,default='Gabon')
    first_name = models.CharField(max_length=120,default="")
    last_name = models.CharField(max_length=120,default="")
    company_name = models.CharField(max_length=120,blank=True,default="")
    address = models.CharField(max_length=250,default="")
    second_address = models.CharField(max_length=250,default="")
    city = models.CharField(max_length=120,default="")
    state = models.CharField(max_length=120,default="")
    postcode = models.CharField(max_length=120,default="")
    email = models.EmailField(default='your_mail@mail.com')
    phone = models.IntegerField(default=100000000)

    def __str__(self):
        return "Customer-Id:{},{} {}".format(self.id,self.first_name,self.last_name)

    def get_absolute_url(self):
        return reverse('customer:view_profile',kwargs={'pk':self.id})


@receiver(post_save,sender = User)
def create_user_profile(sender,instance,created,**kwargs):
    """If New User created, create Profile"""
    if created:
        Profile.objects.create(user=instance)
@receiver
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
