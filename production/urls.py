from django.urls import path
from .views import production

urlpatterns = [
    path('production/', production, name='production'),
]