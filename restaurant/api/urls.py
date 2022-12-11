from rest_framework import routers
from .views import RestaurantViewSet

router = routers.DefaultRouter()

router.register(r'restra', RestaurantViewSet)

urlpatterns = router.urls
