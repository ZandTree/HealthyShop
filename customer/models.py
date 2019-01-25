from django.db import models

COUNTRY_CHOICES = (
    ('USA','USA'),
    ('Gabon','Gabon'),
    ('VK','England'),
    ('Japan','Japan')
)

class Profile(models.Model):
    country = models.CharField(max_length=120,choices=COUNTRY_CHOICES,default='Gabon')
    first_name = models.CharField(max_length=120,default="")
    last_name = models.CharField(max_length=120,default="")
    company_name = models.CharField(max_length=120,blank=True,default="")
    address = models.CharField(max_length=250,default="")
    city = models.CharField(max_length=120,default="")
    state = models.CharField(max_length=120,default="")
    postcode = models.CharField(max_length=120,default="")
    email = models.EmailField(default='your_mail@mail.com')
    phone = models.IntegerField(default=100000000)

    def __str__(self):
        return "Customer-Id:{},{} {}".format(self.id,self.first_name,self.last_name)
