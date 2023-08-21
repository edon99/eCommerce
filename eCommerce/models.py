from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import JSONField
from django.urls import reverse
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# Create your models here.


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN ="ADMIN", 'Admin'
        BUYER ="BUYER", 'Buyer'
        SELLER ="SELLER", 'Seller'
    base_role = Role.BUYER
    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30)
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
    firstName = models.CharField(max_length=100, null=True)
    lastName = models.CharField(max_length=100, null=True)
    date_ordered = models.DateTimeField(default=timezone.now)
    quantity = models.IntegerField(default=1)
    total = models.IntegerField(default=0)
    address = models.CharField(max_length=200, null=True)
    phoneNumber = models.IntegerField()
    class OrderState(models.TextChoices):
        UNPAID ="UNPAID", 'Unpaid'
        PAID ="PAID", 'Paid'
        CANCELED ="CANCELED", 'Canceled'
    base_state = OrderState.UNPAID
    payment_state = models.CharField(max_length=50, choices=OrderState.choices, default=base_state)
    class PaymentMethod(models.TextChoices):
         ON_DELIVERY = "ON DELIVERY",'On Delivery'
         ONLINE = "ONLINE",'Online'
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices, default="ON DELIVERY")
    class Delivery(models.TextChoices):
        SHIPPED ="SHIPPED", 'Shipped'
        DELIVERED ="DELIVERED", 'Delivered'
        CANCELED ="CANCELED", 'Canceled'
        PENDING= "PENDING", 'Pending'
    base_delivery_state = Delivery.PENDING
    delivery_state  = models.CharField(max_length=50, choices=Delivery.choices, default=base_delivery_state)
    def get_absolute_url(self):
         return reverse('product-order-confirm',kwargs={'pk':self.pk})
    
class Notification(models.Model):
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    notification = models.CharField(max_length=300,null=True)
    time = models.DateTimeField(default=timezone.now)
    read_state = models.BooleanField(default=False)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,default=None)

   
class CartQuantities(models.Model):
     cart = models.ForeignKey('Cart',on_delete=models.CASCADE)
     product = models.ForeignKey(Product,on_delete=models.CASCADE)
     quantity = models.IntegerField(default=1)   

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now=True)
    quantities = models.JSONField(default=dict)
   
    def calculate_total(self):
        total_price = Decimal('0.00')
        for product_id, quantity in self.quantities.items():
            try:
                product = Product.objects.get(pk=product_id)
                total_price += product.price * quantity
            except ObjectDoesNotExist:
                
                pass
        self.total_price = total_price
        self.save()


    def __str__(self):
        return f"Cart for {self.user.username}"

    

    
class CartOrder(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    date_ordered = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=200, null=True)
    phoneNumber = models.IntegerField()
    class OrderState(models.TextChoices):
        UNPAID ="UNPAID", 'Unpaid'
        PAID ="PAID", 'Paid'
        CANCELED ="CANCELED", 'Canceled'
    base_state = OrderState.UNPAID
    payment_state = models.CharField(max_length=50, choices=OrderState.choices, default=base_state)
    class PaymentMethod(models.TextChoices):
         ON_DELIVERY = "ON DELIVERY",'On Delivery'
         ONLINE = "ONLINE",'Online'
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices, default="ON DELIVERY")
    class Delivery(models.TextChoices):
        SHIPPED ="SHIPPED", 'Shipped'
        DELIVERED ="DELIVERED", 'Delivered'
        CANCELED ="CANCELED", 'Canceled'
        PENDING= "PENDING", 'Pending'
    base_delivery_state = Delivery.PENDING
    delivery_state  = models.CharField(max_length=50, choices=Delivery.choices, default=base_delivery_state)


def create_orders_from_cart_order(cart_order_instance):
    cart = cart_order_instance.cart
    for product in cart.items.all():
            Order.objects.create(
                product=product,
                buyer=cart_order_instance.cart.user,
                seller=product.seller,  # Adjust as needed
                firstName=cart_order_instance.first_name,
                lastName=cart_order_instance.last_name,
                date_ordered=cart_order_instance.date_ordered,
                quantity=1,
                total=product.price * 1,
                address=cart_order_instance.address,
                phoneNumber=cart_order_instance.phoneNumber,
                payment_state=cart_order_instance.payment_state,
                payment_method=cart_order_instance.payment_method,
                delivery_state=cart_order_instance.delivery_state,
        )
@receiver(post_save, sender=CartOrder)
def create_orders_on_cart_order_save(sender, instance, created, **kwargs):
        if created:
            create_orders_from_cart_order(instance)







    
