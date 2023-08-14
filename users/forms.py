
from django import forms
from eCommerce.models import User ,Order, Product
from users.models import Profile
from django.contrib.auth.forms import UserCreationForm
from eCommerce.widgets import ImagePreviewWidget


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    class Meta():
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.PasswordInput()
    
    class Meta():
        model = User
        fields = ['username','password']
class UserUpdateForm(forms.ModelForm):
      email = forms.EmailField()
      first_name = forms.CharField(max_length=30)
      last_name = forms.CharField(max_length=30)
      class Meta():
        model = User
        fields = ['username','first_name','last_name','email']
    
class ProfileUpdateForm(forms.ModelForm):
     class Meta():
        model = Profile
        fields = ['image']

class SellerForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    role = forms.CharField(widget=forms.HiddenInput(),required=False,  initial="SELLER")
    

    class Meta():
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email','role',)
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])   
        if commit:
            user.save()
        return user
    
class OrderForm(forms.ModelForm):
    firstName = forms.CharField(max_length=50)
    lastName = forms.CharField(max_length=50)
    address = forms.CharField(max_length=200)
    phoneNumber = forms.IntegerField()
    quantity = forms.IntegerField()
    seller = forms.CharField(widget=forms.HiddenInput())
    buyer = forms.CharField(widget=forms.HiddenInput())
    product = forms.CharField(widget=forms.HiddenInput())
    total = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    payment_state = forms.CharField(widget=forms.HiddenInput(),required=False)
    delivery_state = forms.CharField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model = Order
        fields = ['seller', 'buyer', 'product', 'firstName', 'lastName', 'phoneNumber', 'quantity', 'address','payment_state','delivery_state']
    

   

        