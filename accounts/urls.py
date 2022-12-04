from django.urls import path
from .views import signin, logout_view

app_name="accounts"
urlpatterns = [
    path('signin/', signin, name='signin'),
    path('logout/', logout_view, name='logout'),
]
