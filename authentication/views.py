from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from .forms import *
from .models import *


def login(request):
    if request.method == "POST":
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')

        try:
            employee = Employee.objects.get(email_id=email_id)
            if employee.password == password:
                #request.session['employee_id'] = employee.id  # Store employee ID in session
                #request.session['role'] = employee.role  # Store role in session
                if employee.role == 'finance':
                    return redirect('finance') 
                elif employee.role == 'inventory':
                    return redirect('inventory') 
                elif employee.role == 'production':
                    return redirect('production')  
                elif employee.role == 'HR':
                    return redirect('index')  
            else:
                return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

        except Employee.DoesNotExist:
            return render(request, 'accounts/login.html', {'error': 'Employee not found'})
    return render(request, 'accounts/login.html')


#@login_required
def index(request):
    context = {
        'app_name': 'HR',  
        'segment': 'index'
    }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


#@login_required
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


#@login_required
def employee_list(request):
    emp = Employee.objects() 
    context = {
        'app_name': 'HR',
        'emp': emp,
    }
    return render(request, 'home/tables.html', context)


def logout(request):
    # Clear the session data
    #request.session.flush()  # This will remove all session data
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to login page after logout
