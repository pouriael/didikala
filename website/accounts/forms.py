from django.contrib.auth.models import User
from django import forms

from .models import *

# this class for user register form.
class UserregisterForm(forms.Form):
    user_name= forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder':"enter your username"}))
    email= forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'enter your email'}))
    first_name= forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder':"enter your first name"}))
    last_name= forms.CharField(max_length=50 , widget=forms.TextInput(attrs={"placeholder":'enter your last name'}))
    password_1= forms.CharField(max_length=20, widget = forms.PasswordInput(attrs={"placeholder":"enter your password"}))
    password_2= forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'placeholder':'enter your password again'}))

    # user name must not exist in database.
    def clean_user_name(self):
        user = self.cleaned_data["user_name"]
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError("username is exist, please change it !!!")
        return user
    
    # email must not exist in database.
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("this email is exist !!!")
        return email

    # password is to simillar.
    def clean_password_2(self):
        password1 = self.cleaned_data["password_1"]
        password2 = self.cleaned_data["password_2"]
        if password1 != password2:
            raise forms.ValidationError("password not a unique")
        elif len(password2)<3:
            raise forms.ValidationError("this password is short")
        elif not any (x.isupper() for x in password2 ):
            raise forms.ValidationError("you must use capitalize letter")
        return password1

# this class for user login form.
class UserloginForm(forms.Form):
    user = forms.CharField(max_length=50)
    password = forms.CharField(max_length=20)
    remember = forms.BooleanField(required=False,widget=forms.CheckboxInput())

# this class for profile update form user register.
class User_updateform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name']

# this class for profile update form.
class Profile_updateform(forms.ModelForm):
    class Meta:
        model = formprofile
        fields = ['phone','address','profile_image']
        
# this class for login phone form.
class PhoneForm(forms.Form):
    phone = forms.IntegerField()

# this class for code form. 
class CodeForm(forms.Form):
    code = forms.IntegerField()
