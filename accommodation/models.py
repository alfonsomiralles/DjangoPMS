from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Country(models.Model):
    country_name = models.CharField(max_length=100, blank=False, null= False)
    country_code = models.CharField(max_length=6, blank=False, null=False)

    def __str__(self):
        return self.country_name

class City(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    postcode = models.CharField(max_length=5, blank=False, null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name        

class Accommodation(models.Model):
    name = models.CharField(max_length=100, blank=False, null= False)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=False, null= False)
    email= models.EmailField()
    phone = models.CharField(max_length=12, blank=True, null=True)
    mobile = models.CharField(max_length=12, blank=False, null=False)
    image = models.ImageField(blank=False, null=False, upload_to="images/")
    is_active = models.BooleanField(default=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name