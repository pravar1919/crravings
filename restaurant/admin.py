from django.contrib import admin
from .models import Restaurant, Dish, RestaurantRating, DishRating, Tag
# Register your models here.


class DishAdmin(admin.TabularInline):
    model = Dish
    # list_display = ['name','restaurant']

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor']
    inlines = [DishAdmin]

@admin.register(RestaurantRating)
class RestaurantRatingAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'rating','buyer']



@admin.register(DishRating)
class DishRatingAdmin(admin.ModelAdmin):
    list_display = ['dish', 'rating']

admin.site.register(Tag)
admin.site.register(Dish)
