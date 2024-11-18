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
        transactions = Transaction.objects.all()
        context = {
        'app_name': 'Finance',  # Pass app name dynamically
        'transactions': transactions,
    }
        return render(request, 'home/transaction.html',context)


def account(request):
        accounts = Account.objects.all()
        context = {
        'app_name': 'Finance',  # Pass app name dynamically
        'accounts': accounts
    }
        return render(request, 'home/account.html',context)


def invoice(request):
        invoices = Invoice.objects.all()
        context = {
        'app_name': 'Finance',  # Pass app name dynamically
        'invoices': invoices,
    }
        return render(request, 'home/invoice.html',context)


def payment(request):
        payments = Payment.objects.all()
        context = {
        'app_name': 'Finance',  # Pass app name dynamically
        'payments': payments,
    }
        return render(request, 'home/payment.html',context)


def customer(request):
        customers = Customer.objects.all()
        context = {
        'app_name': 'Finance',  # Pass app name dynamically
        'customers': customers,
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
        expenses = Expense.objects.all()
        context = {
        'app_name': 'Finance',  # Pass app name dynamically
        'expenses': expenses
    }
        return render(request, 'home/expense.html',context)


def budget(request):
    budgets = Budget.objects.order_by('-year')  
    context = {
        'app_name': 'Finance', 
        'budgets': budgets,
    }
    return render(request, 'home/budget.html', context)
