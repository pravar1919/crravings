from django.urls import path
from .views import HomePage, RestaurantDetail, Search

app_name = "restaurant"
urlpatterns = [
    path("", HomePage.as_view(), name="homepage"),
    path("q/", Search.as_view(), name="search"),
    path('<int:pk>/', RestaurantDetail.as_view(), name="restra-detail"),
]
