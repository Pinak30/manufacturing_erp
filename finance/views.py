from django.shortcuts import render
from .models import *

# Create your views here.

def finance(request):
        context = {
        'app_name': 'Finance',  # Pass app name dynamically
    }
        return render(request, 'home/finance.html',context)


def generalLedger(request):
        ledger = GeneralLedger.objects.all()
        context = {
        'app_name': 'Finance',  
        'ledger': ledger,
    }
        return render(request, 'home/generalLedger.html',context)


def transaction(request):
        context = {
        'app_name': 'Finance',  # Pass app name dynamically
    }
        return render(request, 'home/transaction.html',context)


def account(request):
        context = {
        'app_name': 'Finance',  # Pass app name dynamically
    }
        return render(request, 'home/account.html',context)


def invoice(request):
        context = {
        'app_name': 'Finance',  # Pass app name dynamically
    }
        return render(request, 'home/invoice.html',context)


def payment(request):
        context = {
        'app_name': 'Finance',  # Pass app name dynamically
    }
        return render(request, 'home/payment.html',context)


def customer(request):
        context = {
        'app_name': 'Finance',  # Pass app name dynamically
    }
        return render(request, 'home/customer.html',context)


def purchaseorder(request):
        orders = PurchaseOrderFinance.objects.all()
        context = {
        'app_name': 'Finance',  
        'orders': orders,
    }
        return render(request, 'home/purchaseorder.html',context)


def expense(request):
        context = {
        'app_name': 'Finance',  # Pass app name dynamically
    }
        return render(request, 'home/expense.html',context)


def budget(request):
        context = {
        'app_name': 'Finance',  # Pass app name dynamically
    }
        return render(request, 'home/budget.html',context)
