
from django import forms
from eCommerce.models import User 
from users.models import Profile
from django.contrib.auth.forms import UserCreationForm




class UserForm(UserCreationForm):
    

    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)
    email = forms.EmailField()
    

    class Meta():
        model = User
        fields = UserCreationForm.Meta.fields + ('firstname', 'lastname', 'email',)

class UserUpdateForm(forms.ModelForm):
      email = forms.EmailField()
      class Meta():
        model = User
        fields = ['username','email']
    
class ProfileUpdateForm(forms.ModelForm):
     class Meta():
        model = Profile
        fields = ['image']
class SellerForm(UserCreationForm):
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)
    email = forms.EmailField()
    role = forms.CharField(widget=forms.HiddenInput(),required=False,  initial="SELLER")
    

    class Meta():
        model = User
        fields = UserCreationForm.Meta.fields + ('firstname', 'lastname', 'email','role',)
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])   
        if commit:
            user.save()
        return user
    

    


   

        