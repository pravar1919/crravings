from django.shortcuts import render, redirect

from .models import Buyer, Vendor
from .forms import SignInForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, FormView
# Create your views here.

def signin(request):
    user = request.user
    if user.is_authenticated:
        vendor = Vendor.objects.filter(email = user.email)
        buyer = Buyer.objects.filter(email = user.email)
        if vendor:
            return redirect('vendor:homepage')
        if buyer:
            return redirect('buyer:homepage')
        if user.is_superuser:
            return redirect('/admin/')
    form = SignInForm(request.POST or None)
    if form.is_valid():
        user = authenticate(username=form.cleaned_data.get("email"), password=form.cleaned_data.get("password"))
        if not user:
            messages.error(request, 'Wrong Credentials.')
            return redirect('accounts:signin')
        login(request, user)
        if user.is_superuser:
            return redirect('/admin/')
        vendor = Vendor.objects.filter(email = user.email)
        buyer = Buyer.objects.filter(email = user.email)
        if not (vendor or buyer):
            messages.error(request, 'Either Signup as Vendor or Buyer')
            return redirect('accounts:signin')
        if vendor:
            return redirect('vendor:homepage')
        if buyer:
            return redirect('buyer:homepage')
    return render(request, 'accounts/signin.html', {"form":form})

def logout_view(request):
    logout(request)
    return redirect('accounts:signin')