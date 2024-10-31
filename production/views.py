from django.shortcuts import render
from .models import *

# Create your views here.

def production(request):
        context = {
        'app_name': 'Production',  # Pass app name dynamically
    }
        return render(request, 'home/production.html',context)


def masterproduction(request):
        context = {
        'app_name': 'Production',  # Pass app name dynamically
    }
        return render(request, 'home/masterproduction.html',context)


def bommanagement(request):
        bom = BOM.objects.all()
        context = {
        'app_name': 'Production',  # Pass app name dynamically
        'bom': bom,
    }
        return render(request, 'home/bommanagement.html',context)


def materialreqplan(request):
        context = {
        'app_name': 'Production',  # Pass app name dynamically
    }
        return render(request, 'home/materialreqplan.html',context)


def workordermanage(request):
        context = {
        'app_name': 'Production',  # Pass app name dynamically
    }
        return render(request, 'home/workordermanage.html',context)