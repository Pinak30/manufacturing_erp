from django import template
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from .forms import *
from .models import *


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            employee = Employee.objects.get(email=email)
            if employee.password == password:
                if employee.role == 'Finance':
                    return redirect('finance') 
                elif employee.role == 'Inventory':
                    return redirect('inventory') 
                elif employee.role == 'Production':
                    return redirect('production')  
                elif employee.role == 'HR':
                    return redirect('index')  
            else:
                return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

        except DoesNotExist:
            return render(request, 'accounts/login.html', {'error': 'Employee not found'})
    return render(request, 'accounts/login.html')


def index(request):
    context = {
        'app_name': 'HR',  
        'segment': 'index'
    }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

def employee_detail(request):
    context = {
        'app_name': 'HR',
        'segment': 'index'
    }
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee details saved successfully!")
            form = SignUpForm() 
    else:
        form = SignUpForm()
    context['form'] = form
    return render(request, 'home/profile.html', context)

def employee_list(request):
    emp = Employee.objects() 
    context = {
        'app_name': 'HR',
        'emp': emp,
    }
    return render(request, 'home/tables.html', context)
