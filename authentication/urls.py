from django.urls import path
from .views import *
# from .views import login_view, register_user
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path('', login, name='login'),
    path('', index, name="index"),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('employee/', employee_detail, name="employee_detail"),
    path('list/', employee_list, name="employee_list"),
]