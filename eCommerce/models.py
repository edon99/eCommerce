from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator 
# from django.contrib.auth.models import User
# Create your models here.


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN ="ADMIN", 'Admin'
        BUYER ="BUYER", 'Buyer'
        SELLER ="SELLER", 'Seller'

    base_role = Role.BUYER
    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)

    def save(self, *args, **kwargs):
        # if not self.pk:
        #     self.role = self.base_role
            return super().save(*args, **kwargs)
        
class Product(models.Model):
    title = models.CharField(max_length=50)
    categorie = models.CharField(max_length=20)
    price = models.IntegerField(default=0, validators=[MinValueValidator(1)])
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
