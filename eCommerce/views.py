from typing import Any, Dict, Optional
from django import views
from django.http import JsonResponse
from django.views import View 
from django.views.generic import TemplateView 
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Product, Order, User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.forms import OrderForm
from .filters import ProductFilter
# Create your views here.


# def home(request) :
#     context = {
#         'products':Product.objects.all()
#     }
#     return render(request, 'eCommerce/home.html', context)

class home(ListView):
    model = Product
    template_name = 'eCommerce/home.html'
    context_object_name = 'products'
    paginate_by= 3

class ProductListView(ListView):
    model = Product
    template_name = 'eCommerce/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = ProductFilter(self.request.GET, queryset=queryset)
        self.filter = filter

        # Apply sorting based on selected option
        sort_option = self.request.GET.get('price', None)
        if sort_option == 'highest':
            queryset = queryset.order_by('-price')
        elif sort_option == 'lowest':
            queryset = queryset.order_by('price')

        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context
    def get_filter(self):
        filter_class = self.get_filter_class()
        return filter_class(self.request.GET, queryset=self.get_queryset())

    def get_filter_class(self):
        return ProductFilter
    
class ProductDetailView(DetailView):
    model = Product

# i changed mixin code so it wont allow regular users to access products/new, ctrl+LoginRequiredMixin for more

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'categorie','image','price']
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)
    
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(product.price * 100),
                        'product_data': {
                            'name': product.title,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/products/order/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })

        
class OrderCreateView(CreateView):
    model = Order
    fields = ['firstName','lastName','phoneNumber','quantity','address']
    def form_valid(self, form):
        product_id = self.kwargs['pk']  # Retrieve the product ID from the URL parameter
        product = Product.objects.get(id=product_id)  # Retrieve the Product instance
        form.instance.buyer = self.request.user
        form.instance.seller = product.seller
        form.instance.product_id = product_id  
        price = Product.objects.get(id=product_id)
        form.instance.total = price.price * form.instance.quantity
        self.object = form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        product_id = self.kwargs['pk']  # Retrieve the product ID from the URL parameter
        product = Product.objects.get(id=product_id)  # Retrieve the Product instance
        context.update({
            "product": product
        })
        return context

    def get_success_url(self):
        product_id = self.kwargs['pk']
        order_id = self.object.id
        return reverse('payment', kwargs={'pk': product_id,'order_id':order_id}) 

def Payment(request,pk, order_id):
    order = Order.objects.get(id=order_id)
    product = Product.objects.get(id=pk)
    stripe = settings.STRIPE_PUBLISHABLE_KEY

   
    return render(request,'eCommerce/order_payment.html',context={'order':order,'product':product,'STRIPE_PUBLIC_KEY':stripe})




class ProductUpdateView(LoginRequiredMixin,UserPassesTestMixin ,UpdateView):
    model = Product
    fields = ['title', 'categorie','image','price']

    def form_valid(self, form):
        form.instance.seller = self.request.user
        print(form.instance.image.url)
        return super().form_valid(form)
    
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.seller:
            return True
        return False
    
class SuccessView(TemplateView):
    template_name ="eCommerce/success.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.success(self.request, 'Your order has been confirmed!')
        return context
    
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    # change this later to that users products list
    success_url = '/sellerHome/'
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.seller:
            return True
        return False
    
def about(request) :
    return render(request, 'eCommerce/about.html')



