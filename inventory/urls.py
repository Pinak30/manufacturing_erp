from django.urls import path
from .views import *

urlpatterns = [
    path('inventory/', inventory, name='inventory'),
]