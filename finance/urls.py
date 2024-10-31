from django.urls import path
from .views import *

urlpatterns = [
    path('finance/', finance, name='finance'),
    path('general_ledger/', generalLedger, name='generalLedger'),
    path('transaction/', transaction, name='transaction'),
    path('account/', account, name='account'),
    path('invoice/', invoice, name='invoice'),
    path('payment/', payment, name='payment'),
    path('customer/', customer, name='customer'),
    path('purchase_order/', purchaseorder, name='purchaseorder'),
    path('expense/', expense, name='expense'),
    path('budget/', budget, name='budget'),
]