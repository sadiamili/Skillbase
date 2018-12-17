from django.contrib.auth import login, logout
#reverse_lazy helps users identify where they should go when a user login or logout
from django.urls import reverse_lazy
#importing view
from django.views.generic import CreateView

#imports different forms (i.e. login/signup)
from . import forms

#connect .py files for login or signing up
#this class will create a new user
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    #when someone have signed up for an account, they will be reversed to a login page
    #it's reverse_lazy because we don't want the system to excute until they hit the submit button
    success_url = reverse_lazy("login")
    #
    template_name = "accounts/signup.html"
