from typing import Any
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import *



class UserCreateView(generic.CreateView):
    model = User
    template_name = 'register.html'
    success_url = '/auth/login'
    form_class = UserCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        print('register')
        return context


class UserLoginView(LoginView):
    template_name = 'register.html'
    redirect_authenticated_user = True
    success_url = '/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


@login_required(login_url='login')
def LogoutView(request):
    logout(request)
    return redirect('home')



class UserDeleteView(generic.DeleteView):
    model = User
    success_url = '/'



class UserUpdateView(generic.UpdateView):
    model = User
    success_url = '/'
    template_name = 'create.html'
    form_class = UserChangeForm

