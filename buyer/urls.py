from django.urls import path
from .views import HomePage, RestaurantDetail

app_name = "buyer"
urlpatterns = [
    path("", HomePage.as_view(), name="homepage"),
    path('<int:pk>/', RestaurantDetail.as_view(), name="restra-detail"),
]
