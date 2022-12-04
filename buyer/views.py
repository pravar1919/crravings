from django.shortcuts import render
from buyer.mixins import BuyerLoginRequiredMixin
from utils.decorators import buyer_login_required
from restaurant.models import Restaurant, RestaurantRating

from django.views.generic import ListView, DetailView
# Create your views here.

class HomePage(BuyerLoginRequiredMixin,ListView):
    model = Restaurant
    template_name= "buyer/home.html"
    context_object_name = 'restras'

    def get_queryset(self):
        queryset = Restaurant.objects.top_rating().order_by('-ratings')
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(HomePage, self).get_context_data(**kwargs)
        context['more_restras'] = Restaurant.objects.exclude(id__in=self.get_queryset().values_list('id', flat=True))
        return context

class RestaurantDetail(DetailView):
    model = Restaurant
    template_name= "buyer/detail.html"
    context_object_name = 'restra'
    queryset = Restaurant.objects.rating()

    def get_context_data(self, **kwargs):
        print(kwargs)
        type = self.request.GET.get('type')
        if type:
            type=type.upper()
        context = super(RestaurantDetail, self).get_context_data(**kwargs)
        context['type'] = type
        context['dishes'] = self.get_queryset().get(id=kwargs['object'].id).dishes.type(type).all()
        context['reviews'] = RestaurantRating.objects.filter(restaurant=kwargs['object']).order_by('-created_at')
        return context