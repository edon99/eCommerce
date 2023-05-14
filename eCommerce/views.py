from django.shortcuts import render
from.models import Product
from django.http import HttpResponse
# Create your views here.


def home(request) :
    context = {
        'products':Product.objects.all()
    }
    return render(request, 'eCommerce/home.html', context)
 
def about(request) :
    return render(request, 'eCommerce/about.html')



