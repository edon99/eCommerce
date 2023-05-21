import json
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from eCommerce.filters import ProductFilter
from django.contrib.auth import authenticate, login ,logout
from .forms import UserForm ,SellerForm , UserUpdateForm, ProfileUpdateForm
from eCommerce.models import User
from eCommerce.models import Product
import matplotlib.pyplot as plt
import io
import urllib, base64
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST or None)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created!')
            return redirect('login')

        
    else:       
        form = UserForm() 
    return render(request, 'users/signup.html',{'form':form})



def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        sellers = User.objects.filter(role="SELLER")
        admins = User.objects.filter(is_staff=True)
        if user is not None: 
            for seller in sellers:
                if seller.username == username :
                    login(request, user)
                    return redirect('sellerHome')
                    
            for admin in admins :
                if admin.username == username:
                    user.is_authenticated == True
                    return redirect('admin-dashboard') 
                    
            login(request, user)
            return redirect('site-home')              
        else:
            messages.success(request,f'There was an error')
            return redirect('login')
    
    else:
        return render(request, 'users/login.html',{})
    
    

def logout_user(request):
    logout(request)
    return redirect('site-home')

def sellerSignup(request):
    data = request.POST.copy()
    data['role']="SELLER"
    form=SellerForm(data)
    print(data)
    if request.method == 'POST':
        form = SellerForm(data or None)
        if form.is_valid():
            print("this is after validation "+ data["role"])
            form.save()
            messages.success(request, f'Your account has been created!')
            return redirect('login')
    else:       
        form = SellerForm() 
    return render(request, 'users/sellerSignup.html',{'form':form})

def sellerHome(request):
    context={
       'products':Product.objects.filter(seller_id=request.user)
    }
    return render(request, 'users/sellerHome.html', context)

class ProductListView(ListView):
    model = Product
    template_name = 'users/sellerProducts.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        queryset = Product.objects.filter(
            seller_id=self.request.user
        )
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
    # we can add .order_by('-date_posted') after closing pare
    
def analytics(request) :
    product = Product.objects.all()
    context = {
        'products':product
    }
    return render(request, 'users/sellerAnalytics.html', context)

def admin_dash(request):
    products_nb = Product.objects.all()
    categories={}
    for product in products_nb:
        category = product.categorie
        if category in categories:
            categories[category] +=1
        else:
            categories[category] =1
    categoriesJson = json.dumps(categories)

    users = User.objects.all()
    roles_data = {'BUYER': 0, 'SELLER': 0}
    for user in users:
        role = user.role
        if role in roles_data:
            roles_data[role] += 1

    
    roles_data_json = json.dumps(roles_data)
    
    context = {
        'products':Product.objects.all(),
        'sellers':User.objects.filter(role="SELLER").count(),
        'users':User.objects.all().exclude(is_staff=True),
        'products_count':Product.objects.count(),
        'products_nb':categoriesJson,
        'users_count':User.objects.count(),
        'categories':Product.objects.values_list('categorie',flat=True).distinct(),
        'roles':roles_data_json,
    }
    


    return render(request, 'users/adminDash.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid:
           u_form.save()
           p_form.save() 
           messages.success(request,f'Your Profile has been updated!')
           return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'users/profile.html', context)


