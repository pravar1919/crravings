from django.shortcuts import redirect, render
from buyer.mixins import BuyerLoginRequiredMixin
from utils.decorators import buyer_login_required
from .models import Dish, Restaurant, RestaurantRating, City
from django.views import View
from django.views.generic import ListView, DetailView
from accounts.signals import object_viewed_signal
from accounts.models import ObjectViewed
from django.db.models import Avg,Count
from base.constants import Round
# Create your views here.

def get_page_tracking(request, obj):
    if request.user.is_authenticated:
        object_viewed_signal.send(obj.__class__,instance=obj,request=request)
class HomePage(BuyerLoginRequiredMixin,ListView):
    model = Restaurant
    template_name= "buyer/home.html"
    context_object_name = 'restras'

    def get_queryset(self):
        queryset = Restaurant.objects.top_rating().order_by('-ratings')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['more_restras'] = Restaurant.objects.exclude(id__in=self.get_queryset().values_list('id', flat=True)).order_by("?")
        if self.request.user.is_authenticated:
            history_qs = ObjectViewed.objects.filter(user=self.request.user, model_name__contains="restaurant").order_by('-timestamp')
            if history_qs:
                h = [i['model_product_id'] for i in history_qs.values('model_product_id')[:5] if i['model_product_id']]
                context['history'] = Restaurant.objects.rating().filter(id__in=h)
        context['cities'] = City.objects.all()
        return context

class Search(View):
    def get(self, request, *args, **kwargs):
        context = {}
        query = request.GET.get("q")
        if query:
            context['search_results'] = Restaurant.objects.rating().filter(name__icontains=query)
            context['query'] = query
        else:
            return redirect("restaurant:homepage")
        get_page_tracking(self.request, self.request.user)
        return render(request, "buyer/home.html", context)

class RestaurantDetail(DetailView):
    model = Restaurant
    template_name= "buyer/detail.html"
    context_object_name = 'restra'
    queryset = Restaurant.objects.rating()

    def get_context_data(self, **kwargs):
        type = self.request.GET.get('type')
        if type:
            type=type.upper()
        context = super(RestaurantDetail, self).get_context_data(**kwargs)
        context['type'] = type
        dishes = self.get_queryset().get(id=self.object.id).dishes.type(type).all()
        context['dishes'] = dishes
        print(dishes.values_list('id'))
        context['dishe_rating'] = Dish.objects.filter(id__in=dishes.values_list('id')).annotate(ratings=Round(Avg('rating__rating')), users=Count('rating__buyer'))#.rating.all()
        for i in Dish.objects.filter(id__in=dishes.values_list('id')):
            print(i)
        context['reviews'] = RestaurantRating.objects.filter(restaurant=kwargs['object']).order_by('-created_at')
        get_page_tracking(self.request, self.request.user)
        return context