from django.urls import path
from .views import HomePage, RestaurantDetail, Search, home

app_name = "restaurant"
urlpatterns = [
    path("", home, name="home"),
    path("home/<str:city>/", HomePage.as_view(), name="homepage"),
    path('home/<str:city>/<int:pk>/', RestaurantDetail.as_view(), name="restra-detail"),
    path("q/<str:city>/", Search.as_view(), name="search"),
]
