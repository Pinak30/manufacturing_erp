from django.urls import path
from .views import finance

urlpatterns = [
    path('finance/', finance, name='finance'),
]