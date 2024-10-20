from django.shortcuts import render

# Create your views here.
def inventory(request):
    context = {
        'app_name': 'Inventory',  # Pass app name dynamically
    }
    return render(request, 'home/inventory.html',context)