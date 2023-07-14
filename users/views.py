import json
from django.core.paginator import Paginator
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView,UpdateView,DeleteView
from eCommerce.filters import ProductFilter
from django.contrib.auth import authenticate, login ,logout
from .forms import UserForm ,SellerForm , UserUpdateForm, ProfileUpdateForm
from eCommerce.models import User, Product, Order, Notification
from django.db.models import Max,Avg,Min,Count,Sum
from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from django.utils import timezone



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
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    
    else:
        return render(request, 'users/login.html')
    
    

def logout_user(request):
    logout(request)
    return redirect('login')



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
    total_revenue = Order.objects.filter(seller_id=request.user).aggregate(total_sum=Sum('total')).get('total_sum')
    revenue = total_revenue or 0
    context={
       
        'products_count':Product.objects.filter(seller_id=request.user).count(),
        'products':Product.objects.filter(seller_id=request.user)[:3],
        'orders_count':Order.objects.filter(seller=request.user).count(),
        'orders':Order.objects.filter(seller=request.user).order_by('-date_ordered')[:5],
        'revenue':revenue
    }
    return render(request, 'users/sellerHome.html', context)

def sellerAnalytics(request):
    top_products = Product.objects.filter(seller=request.user) \
        .annotate(order_count=Count('order')) \
        .order_by('-order_count')[:5]

    most_expensive_products = Product.objects.filter(seller=request.user) \
        .order_by('-price')[:5]

    paginator_expensive = Paginator(most_expensive_products, 4)
    page_number_expensive = request.GET.get('page_expensive')
    page_obj_expensive = paginator_expensive.get_page(page_number_expensive)

    highest_orders = Order.objects.filter(seller=request.user) \
        .order_by('-total')

    paginator_highest_orders = Paginator(highest_orders, 4)
    page_number_highest_orders = request.GET.get('page_highest_orders')
    page_obj_highest_orders = paginator_highest_orders.get_page(page_number_highest_orders)

    order_distribution_by_category = Order.objects.filter(seller=request.user) \
        .values('product__categorie') \
        .annotate(order_count=Count('id')) \
        .order_by('-order_count')

    best_selling_months = Order.objects.annotate(month=ExtractMonth('date_ordered')) \
        .values('month') \
        .annotate(total_sales=Sum('total')) \
        .order_by('-total_sales')

    total_revenue = Order.objects.filter(seller_id=request.user).aggregate(total_sum=Sum('total')).get('total_sum')
    revenue = total_revenue or 0

    current_time = timezone.now()
    time_48_hours_ago = current_time - timezone.timedelta(hours=48)
    recent_orders = Order.objects.filter(seller = request.user)\
        .filter(date_ordered__gte=time_48_hours_ago).count()

    shipped = Order.objects.filter(seller = request.user)\
        .filter(delivery_state = 'SHIPPED').count()
    
    delivered = Order.objects.filter(seller = request.user)\
        .filter(delivery_state = 'DELIVERED').count()
    
    canceled = Order.objects.filter(seller = request.user)\
        .filter(delivery_state = 'CANCELED').count()
    
    context = {
        'products_count': Product.objects.filter(seller_id=request.user).count(),
        'top_products': top_products,
        'most_expensive_products': most_expensive_products,
        'page_obj_expensive': page_obj_expensive,
        'highest_orders': highest_orders,
        'page_obj_highest_orders': page_obj_highest_orders,
        'order_distribution_by_category': order_distribution_by_category,
        'best_selling_months': best_selling_months,
        'products_count': Product.objects.filter(seller_id=request.user).count(),
        'orders_count': Order.objects.filter(seller=request.user).count(),
        'revenue': revenue,
        'customers':Order.objects.filter(product__seller=request.user).values('buyer').distinct().count(),
        'recentOrders':recent_orders,
        'shipped':shipped,
        'delivered':delivered,
        'canceled':canceled,
    }

    return render(request, 'users/sellerAnalytics.html', context)


def sellerOrders(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        notification = Notification.objects.filter(order=order_id).first()
        notification.read_state=True
        notification.save()
    context={
        'orders':Order.objects.filter(seller=request.user).order_by('-date_ordered'),
    }
    return render(request, 'users/sellerOrders.html', context)

def OrderUpdate(request,pk):

    order = get_object_or_404(Order, id=pk)

   

    if request.method=='POST':
         delivery_state = request.POST.get('delivery-state')
         payment_state = request.POST.get('payment-state')

         order.delivery_state = delivery_state
         order.payment_state = payment_state
         order.save()

         return redirect('seller-orders')
    
    
    buyer = order.buyer

    Notification.objects.create(receiver=buyer, notification="Your Order has been updated", order=order )
    context = {
        'order': order
    }
    return render(request, 'users/orderUpdate.html', context)

class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    # change this later to that users products list
    success_url = '/sellerOrders/'
    
    def test_func(self):
        order = self.get_object()
        if self.request.user == order.seller:
            return True
        return False


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
    
def analytics(request):
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
        'orders_count':Order.objects.all().count(),
        'sellers':User.objects.filter(role="SELLER").count(),
        'users':User.objects.all().exclude(is_staff=True),
        'products_count':Product.objects.count(),
        'products_nb':categoriesJson,
        'users_count':User.objects.count(),
        'categories':Product.objects.values_list('categorie',flat=True).distinct(),
        'products_max':Product.objects.aggregate(max_price=Max("price"))["max_price"],
        'products_avg':Product.objects.aggregate(avg_price=Avg("price"))["avg_price"],
        'products_min':Product.objects.aggregate(min_price=Min("price"))["min_price"],
        'most_ordered_product':Product.objects.annotate(order_count=Count('order')).order_by('-order_count').first(),
        'seller_with_most_orders': User.objects.filter(product__isnull=False).annotate(order_count=Count('product__order')).order_by('-order_count').first(),
        'total_orders_price': Order.objects.aggregate(total_price=Sum('product__price'))["total_price"],
        'roles':roles_data_json,
    }
    return render(request, 'users/sellerDashboard.html', context)

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
        'orders_count':Order.objects.all().count(),
        'sellers':User.objects.filter(role="SELLER").count(),
        'users':User.objects.all().exclude(is_staff=True),
        'products_count':Product.objects.count(),
        'products_nb':categoriesJson,
        'users_count':User.objects.count(),
        'categories':Product.objects.values_list('categorie',flat=True).distinct(),
        'products_max':Product.objects.aggregate(max_price=Max("price"))["max_price"],
        'products_avg':Product.objects.aggregate(avg_price=Avg("price"))["avg_price"],
        'products_min':Product.objects.aggregate(min_price=Min("price"))["min_price"],
        'most_ordered_product':Product.objects.annotate(order_count=Count('order')).order_by('-order_count').first(),
        'seller_with_most_orders': User.objects.filter(product__isnull=False).annotate(order_count=Count('product__order')).order_by('-order_count').first(),
        'total_orders_price': Order.objects.aggregate(total_price=Sum('product__price'))["total_price"],
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


