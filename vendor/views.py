from django.shortcuts import render
from utils.decorators import vendor_login_required
# Create your views here.

@vendor_login_required
def homepage(request):
    return render(request, "vendor/home.html")