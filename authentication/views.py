from django import template
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import *
from .models import *


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Fetch the employee by email
            employee = Employee.objects.get(email=email)

            # Check if the password matches (you may want to hash passwords in a real application)
            if employee.password == password:
                # Redirect based on department
                if employee.department == 'Finance':
                    return redirect('finance')  # Adjust the finance URL as needed
                elif employee.department == 'Inventory':
                    return redirect('inventory')  # Adjust the inventory URL as needed
                elif employee.department == 'Production':
                    return redirect('production')  # Adjust the production URL as needed
                elif employee.department == 'HR':
                    return redirect('index')  # Redirect to a default page
            else:
                return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

        except DoesNotExist:
            return render(request, 'accounts/login.html', {'error': 'Employee not found'})
    return render(request, 'accounts/login.html')

# @login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

def employee_detail(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee details saved successfully!")
            form = SignUpForm()  # Reset the form
    else:
        form = SignUpForm()

    return render(request, 'home/profile.html', {'form': form})

def employee_list(request):
    emp = Employee.objects()  # Fetch all Employee documents
    context = {
        'emp': emp,
    }
    return render(request, 'home/tables.html', context)

# @login_required(login_url="/login/")
# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:

#         load_template = request.path.split('/')[-1]

#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))
#         context['segment'] = load_template

#         html_template = loader.get_template('home/' + load_template)
#         return HttpResponse(html_template.render(context, request))

#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template('home/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('home/page-500.html')
#         return HttpResponse(html_template.render(context, request))
