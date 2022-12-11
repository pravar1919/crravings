from rest_framework import viewsets
from restaurant.models import Restaurant
from .serializers import RestaurantSerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        qs = Restaurant.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            qs = qs.filter(name__icontains=name)
        return qs