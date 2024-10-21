from django.urls import path
from .views import *

urlpatterns = [
    path('inventory/', inventory, name='inventory'),
    path('stock/', stock_qty, name='stock_qty'),
    path('stock_qty', stock_qty_raw, name='stock_qty_raw'),
    path('stock_coverage/', stock_coverage, name='stock_coverage'),
    # path('milk_procurementation/', milk_procurementation, name='milk_procurementation'),
    path('sku/', active_sku, name='active_sku'),
    path('all_product/', all_product_list, name='all_product_list'),
    path('inventory_value/', inventory_value, name='inventory_value'),
    path('inventory_transaction/', inventory_transaction_summary, name='inventory_transaction_summary'),
    # path('stoke_movement_analysis/', stoke_movement_analysis, name='stoke_movement_analysis'),
    # path('open_purchase_orders/', open_purchase_orders, name='open_purchase_orders'),
    # path('cycle_count/', cycle_count_stock_audit, name='cycle_count_stock_audit'),
    # path('historic_trend_analysis/', historic_trend_analysis, name='historic_trend_analysis'),
]