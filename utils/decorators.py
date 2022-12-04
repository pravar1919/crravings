from django.shortcuts import redirect
from accounts.models import Buyer,Vendor


def buyer_login_required(function):
    def wrapper(request, *args, **kw):
        user=request.user
        buyer = Buyer.objects.filter(email=user.email)
        if not buyer:
            return redirect('accounts:signin')
        return function(request, *args, **kw)
    return wrapper

def vendor_login_required(function):
    def wrapper(request, *args, **kw):
        user=request.user
        vendor = Vendor.objects.filter(email=user.email)
        if not vendor:
            return redirect('accounts:signin')
        return function(request, *args, **kw)
    return wrapper