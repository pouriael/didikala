from django.contrib.auth.models import User
from django import forms
from .models import *



class SearchForm(forms.Form):
    search = forms.CharField(max_length=300)
