from django.shortcuts import render

# Create your views here.

def production(request):
    return render(request, 'production.html')