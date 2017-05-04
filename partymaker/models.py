from django.db import models

# Create your models here.


class Drink(models.Model):
    title = models.CharField(max_length=255, unique=True)


class User(models.Model):
    photo = models.ImageField()
    name = models.CharField(max_length=255)


class Order(models.Model):
    user = models.OneToOneField(User)
    is_member = models.BooleanField()
    drink = models.ForeignKey(Drink)
