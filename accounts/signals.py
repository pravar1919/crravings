
from django.dispatch import Signal

object_viewed_signal = Signal("request")

user_logged_in = Signal("request")