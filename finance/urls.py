from django.urls import path
from .views import *

urlpatterns = [
    path('finance/', finance, name='finance'),
]