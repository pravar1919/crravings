from django.urls import path
from .views import signin, logout_view, profile

app_name="accounts"
urlpatterns = [
    path('signin/', signin, name='signin'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
]
