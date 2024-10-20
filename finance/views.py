from django.shortcuts import render

# Create your views here.

def finance(request):
        context = {
        'app_name': 'Finance',  # Pass app name dynamically
    }
        return render(request, 'home/finance.html',context)
