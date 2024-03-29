from decimal import Decimal
import json
from typing import Any, Dict, Optional
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django import views
from django.http import JsonResponse
from django.views import View 
from django.views.generic import TemplateView 
import stripe
from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Product, Order, Cart,Notification,CartOrder
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.forms import CartOrderForm
from .filters import ProductFilter

    
def home(request):
    search = request.GET.get('search')
    if search: 
        data = Product.objects.filter(title__icontains=search)
    else:
        data = Product.objects.all()

    context = {
        'products': data[:3], 
        'data': data,
    }

    return render(request,'eCommerce/home.html',context)
    # https://www.youtube.com/watch?v=iFlSrEuyl8I&ab_channel=KenBroTech SEARCH FUNCTION THIS IS NEXT

def orders(request):
    
    if request.method == 'POST':
        notif_id = request.POST.get('notif_id')
        notification = get_object_or_404(Notification, id=notif_id)
        notification.read_state=True
        notification.save()
    orders = Order.objects.filter(buyer= request.user).order_by('-date_ordered')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
   

    return render(request,'eCommerce/orders.html',context={'orders':orders,})
    


from django.db.models import Q

class ProductListView(ListView):
    model = Product
    template_name = 'eCommerce/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()

        
        product_filter = ProductFilter(self.request.GET, queryset=queryset)
        queryset = product_filter.qs


        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(categorie__icontains=search_query) |  
                Q(title__icontains=search_query)      
            )

        
        sort_option = self.request.GET.get('price')
        if sort_option == 'highest':
            queryset = queryset.order_by('-price')
        elif sort_option == 'lowest':
            queryset = queryset.order_by('price')

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = ProductFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = filter
        return context

    
class ProductDetailView(DetailView):
    model = Product

# i changed mixin code so it wont allow regular users to access products/new, ctrl+LoginRequiredMixin for more

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'categorie','image','price']
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)
    
def add_to_cart(request,product_id):
    product= Product.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.items.add(product)
    quantities = cart.quantities
    quantities[product_id] = 1
    cart.quantities = quantities
    cart.calculate_total()
    cart.save()
    return JsonResponse({'success': True})

def delete_from_cart(request,product_id):
    product= Product.objects.get(pk=product_id)
    cart= Cart.objects.get(user=request.user)
    quantities = cart.quantities
    key = str(product_id)
    quantities.pop(key)
    cart.quantities = quantities
    cart.items.remove(product)
    cart.calculate_total()
    cart.save()
    return JsonResponse({'success': True})


def update_cart_quantities(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            updated_quantities = data.get('updated_quantities', None)
            
            if updated_quantities:
                cart = Cart.objects.get(user=request.user)
                quantities = cart.quantities
                
                for updated_item in updated_quantities:
                    product_id = updated_item['product_id']
                    quantity = updated_item['quantity']
                    quantities[product_id] = quantity

                cart.quantities = quantities
                cart.calculate_total()  
                cart.save()

                return JsonResponse({'success': True})

        except json.JSONDecodeError:
            print('shit wild')
            pass  

    return JsonResponse({'success': False})



def cart_items(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()
    cart_quantities = cart.quantities
    return render (request, 'eCommerce/cartItems.html',context={'cart': cart,'cart_items':cart_items,'quantities':cart_quantities})

def cart_order(request):
    if request.method == 'POST':
        
        form = CartOrderForm(request.POST)
        cart = Cart.objects.get(user=request.user)
        if form.is_valid():
                
                new_order = form.save(commit=False)
                new_order.cart = cart
                new_order.save()
                
                return redirect('cart-payment',order_id = new_order.id)        
        
    else:
        form = CartOrderForm() 

    return render(request, 'eCommerce/cartOrder.html', {'form': form})


def cartPayment(request,order_id):

    order = CartOrder.objects.get(pk=order_id)
    cart = order.cart
    cart_items = cart.items.all()
    quantities = cart.quantities
    return render (request,'eCommerce/cartPayment.html',context={'order':order,'cart':cart,'cart_items':cart_items,'quantities':quantities})
    

        
    
    


    
    






    
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order = Order.objects.get(id=order_id)
        order.payment_method = "ONLINE"
        order.payment_state = "PAID" #pour le moment
        product= order.product
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
            success_url=YOUR_DOMAIN + '/products/order/success/'+str(order_id)+'/' ,
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })
    
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        
        return HttpResponse(status=400)

    
    if event.type == "checkout.session.completed":
        session = event.data.object

        
        order_id = session.get("metadata", {}).get("product_id")
        if not order_id:
            
            return HttpResponse(status=400)

    
        order = Order.objects.get(id=order_id)
        order.payment_state = "PAID"
        order.payment_method = "ONLINE"
        order.save()

    
    return HttpResponse(status=200)

        
class OrderCreateView(CreateView):
    model = Order
    fields = ['firstName','lastName','phoneNumber','quantity','address']
    def form_valid(self, form):
        product_id = self.kwargs['pk']  
        product = Product.objects.get(id=product_id)
        form.instance.buyer = self.request.user
        form.instance.seller = product.seller
        form.instance.product_id = product_id  
        price = Product.objects.get(id=product_id)
        form.instance.total = price.price * form.instance.quantity
        self.object = form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        product_id = self.kwargs['pk'] 
        product = Product.objects.get(id=product_id) 
        context.update({
            "product": product
        })
        return context

    def get_success_url(self):
        product_id = self.kwargs['pk']
        order_id = self.object.id
        return reverse('payment', kwargs={'pk': product_id,'order_id':order_id}) 
    
def OrderCancel(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            if order.payment_state in ['UNPAID', 'CANCELED']:
                order.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Order cannot be canceled. Contact the seller for more information.'})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def Payment(request,pk, order_id):
    order = Order.objects.get(id=order_id)
    product = Product.objects.get(id=pk)
    seller = order.seller.id
    stripe = settings.STRIPE_PUBLISHABLE_KEY

   

    return render(request,'eCommerce/order_payment.html',context={'order':order,'product':product,'seller':seller,'STRIPE_PUBLIC_KEY':stripe})

 
class ProductUpdateView(LoginRequiredMixin,UserPassesTestMixin ,UpdateView):
    model = Product
    fields = ['title', 'categorie','image','price']
    template_name = 'eCommerce/product_form.html'
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
    template_name = "eCommerce/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        order = get_object_or_404(Order, id=self.kwargs['pk'])

        seller = order.seller
        buyer = order.buyer

        Notification.objects.create(receiver=seller, notification="You have Received a new Order from " + str(buyer), order=order )
        
        
        # Customize the notification content and other details as per your requirements

        messages.success(self.request, 'Your order has been confirmed!')
        return context

class CancelView(TemplateView):
    template_name = "eCommerce/cancel.html"

    
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/sellerHome/'
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.seller:
            return True
        return False
    



