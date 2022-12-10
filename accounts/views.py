from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from restaurant.models import Restaurant
from .models import Buyer, Vendor
from .forms import SignInForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from accounts.signals import object_viewed_signal
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, FormView

def get_page_tracking(request, obj):
    ############### User Signal #######################
    object_viewed_signal.send(obj.__class__,instance=obj,request=request)
    ###################################################

def signin(request):
    user = request.user
    if user.is_authenticated:
        vendor = Vendor.objects.filter(email = user.email)
        buyer = Buyer.objects.filter(email = user.email)
        if vendor:
            return redirect('vendor:homepage')
        if buyer:
            return redirect('restaurant:homepage', "Ahmedabad")
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
            return redirect('restaurant:homepage', "Ahmedabad")
    return render(request, 'accounts/signin.html', {"form":form})

def logout_view(request):
    logout(request)
    return redirect('accounts:signin')

@login_required
def profile(request):
    profile = Buyer.objects.get(email=request.user)
    context = {
        "profile": profile
    }
    context['favourates'] = Restaurant.objects.rating().favourities(request.user)
    get_page_tracking(request, request.user)
    return render(request, 'accounts/profile.html', context)
