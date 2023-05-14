from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from .forms import UserForm ,SellerForm
from eCommerce.models import User
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST or None)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created!')
            return redirect('login')
    else:       
        messages.success(request,f'sum is wrong22')
        form = UserForm() 
    return render(request, 'users/signup.html',{'form':form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        sellers = User.objects.filter(role="SELLER")
        if user is not None: 
            for seller in sellers:
                if seller.username == username :
                    login(request, user)
                    return redirect('sellerHome')
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
        # form = SellerForm(request.POST or None)
        form = SellerForm(data or None)
        if form.is_valid():
            print("this is after validation "+ data["role"])
            form.save()
            messages.success(request, f'Your account has been created!')
            return redirect('login')
    else:       
        messages.success(request,f'sum is wrong22')
        form = SellerForm() 
    return render(request, 'users/sellerSignup.html',{'form':form})




def sellerHome(request):
    return render(request, 'users/sellerHome.html')

@login_required
def profile(request):
    return render(request,'users/profile.html')


