from django.contrib import admin
from eCommerce.models import Product
from django.contrib.auth.admin import UserAdmin
from eCommerce.models import User
# Register your models here.

admin.site.register(Product)
admin.site.register(User)