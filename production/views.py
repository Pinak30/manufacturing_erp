from django.shortcuts import render

# Create your views here.

def production(request):
        context = {
        'app_name': 'Production',  # Pass app name dynamically
    }
        return render(request, 'home/production.html',context)