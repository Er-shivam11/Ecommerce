from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Car(models.Model):
    # user = models.ForeignKey(
    #     User, on_delete=models.SET_NULL, null=True, blank=True)
    car_name = models.CharField(max_length=100)
    car_details = models.TextField()
    car_image = models.ImageField(upload_to="cars", default="")


class sign_up(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
