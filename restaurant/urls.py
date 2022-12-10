from django.urls import path
from .views import HomePage, RestaurantDetail, Search

app_name = "restaurant"
urlpatterns = [
    path("q/", Search.as_view(), name="search"),
    path("<str:city>/", HomePage.as_view(), name="homepage"),
    path('<str:city>/<int:pk>/', RestaurantDetail.as_view(), name="restra-detail"),
]
