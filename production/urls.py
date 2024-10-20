from django.urls import path
from .views import *

urlpatterns = [
    path('production/', production, name='production'),
]