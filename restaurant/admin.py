from django.contrib import admin
from .models import Restaurant, Dish, RestaurantRating, DishRating, Tag, FavouritiesRestaurants, City
# Register your models here.


class DishAdmin(admin.TabularInline):
    model = Dish
    # list_display = ['name','restaurant']

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'vendor']
    inlines = [DishAdmin]

@admin.register(RestaurantRating)
class RestaurantRatingAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'rating','buyer']



@admin.register(DishRating)
class DishRatingAdmin(admin.ModelAdmin):
    list_display = ['dish', 'rating']

admin.site.register(Tag)
admin.site.register(Dish)
admin.site.register(FavouritiesRestaurants)
admin.site.register(City)
