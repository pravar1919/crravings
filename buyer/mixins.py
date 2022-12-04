from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from accounts.models import Buyer

class BuyerLoginRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        user=request.user
        buyer = Buyer.objects.filter(email=user)
        if not (buyer or user.is_anonymous):
            return redirect('accounts:signin')
        return super().dispatch(request, *args, **kwargs)