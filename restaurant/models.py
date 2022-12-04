from django.db.models import Avg, Count
from django.db import models

from accounts.models import Buyer, Vendor
from base.constants import Round, Type, RestraType

class RestaurantQuerySet(models.QuerySet):
    def rating(self):
        qs = self.annotate(ratings=Round(Avg('rating__rating')), users=Count('rating__buyer'))
        return qs
    
    def top_rating(self):
        qs = self.rating().filter(ratings__gte=2.5)
        return qs

class RestaurantManager(models.Manager):
    def get_queryset(self):
        return RestaurantQuerySet(self.model, using=self._db)

    def rating(self):
        return self.get_queryset().rating()

    def top_rating(self):
        return self.get_queryset().top_rating()

class Restaurant(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=255)
    desc = models.TextField(null=True, blank=True)
    location = models.URLField()
    active = models.BooleanField(default=True)
    type = models.CharField(choices=RestraType.choices(), max_length=10)
    open_time = models.TimeField()
    close_time = models.TimeField()
    temporary_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RestaurantManager()

class DishQuerySet(models.QuerySet):
    def type(self, type):
        if type:
            qs = self.filter(type=type)
        else:
            qs = self
        return qs
    
    def sort(self,order):
        if order == "desc":
            qs = self.order_by('base_price')
        else:
            qs = self.order_by('-base_price')
        return qs
class DishManager(models.Manager):
    def get_queryset(self):
        return DishQuerySet(self.model, using=self._db)

    def type(self, type):
        return self.get_queryset().type(type)
    
    def sort(self, order):
        return self.get_queryset().sort(order)

class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='dishes')
    name = models.CharField(max_length=255)
    type = models.CharField(choices=Type.choices(), max_length=10)
    base_price = models.IntegerField()
    shot_description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='dishes_thumbnail/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = DishManager()

class RestaurantRating(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='rating')
    rating = models.FloatField()
    comments = models.TextField(blank=True, null=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='restra_rating')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DishRating(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='rating')
    rating = models.FloatField()
    comments = models.TextField(blank=True, null=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='dish_rating')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)