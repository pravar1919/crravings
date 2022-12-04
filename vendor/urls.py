from django.urls import path
from .views import homepage

app_name = "vendor"
urlpatterns = [
    path("", homepage, name="homepage")
]
