from .models import City

def say_hello(request):
    cities = City.objects.all()
    return {
        'cities':cities,
    }