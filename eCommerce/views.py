from typing import Optional
from django.shortcuts import render, redirect
from.models import Product, Order, User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
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
    
@login_required
def OrderProduct(request):
   
    if request.method == 'POST':
       
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        
        
        buyer_id = request.user.id
        buyer = User.objects.get(id=buyer_id)
        
        
        seller_id = product.seller_id
        seller = User.objects.get(id=seller_id)
        
        
        order = Order.objects.create(product=product, buyer=buyer, seller=seller)
        
        
        return render(request, 'eCommerce/product_order.html')
    
    
    return render(request, 'eCommerce/product_detail.html')

class ProductDetailView(DetailView):
    model = Product
# i changed mixin code so it wont allow regular users to access products/new, ctrl+LoginRequiredMixin for more

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'categorie','image','price']
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)
    
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
    
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    # change this later to that users products list
    success_url = '/sellerHome/'
    def test_func(self):

        product = self.get_object()
        if self.request.user == product.seller:
            return True
        return False
    
# def analytics(request) :
#     product = Product.objects.all()
#     context = {
#         'products':product
#     }
#     return render(request, 'users/sellerAnalytics.html', context)
    
    
   

def about(request) :
    return render(request, 'eCommerce/about.html')



