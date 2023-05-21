from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.urls import reverse
from django.utils import timezone
from PIL import Image
# from django.contrib.auth.models import User
# Create your models here.


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN ="ADMIN", 'Admin'
        BUYER ="BUYER", 'Buyer'
        SELLER ="SELLER", 'Seller'

    base_role = Role.BUYER
    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
            return super().save(*args, **kwargs)
    
        
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('shoes', 'Shoes'),
        ('tops', 'Tops'),
        ('hats', 'Hats'),
    ]
    title = models.CharField(max_length=50)
    categorie = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(default=0,max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    image = models.ImageField(default='download.jpg', upload_to='product_pics')
    date_created = models.DateTimeField(default=timezone.now)
    seller = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
         return reverse('product-detail',kwargs={'pk':self.pk})
    
class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE,related_name='buyer')
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(default=timezone.now)
    number = models.IntegerField(default=1)
    
  
    
