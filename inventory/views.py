from django.shortcuts import render

# Create your views here.
def inventory(request):
    context = {
        'app_name': 'Inventory',
    }
    return render(request, 'home/inventory.html',context)

def stock_qty(request):
        context = {
        'app_name': 'Inventory',
    }
        # fetch only finished products and send via dictionary give name>> products
        return render(request, 'home/stock_qty.html',context)

def stock_qty_raw(request):
        context = {
        'app_name': 'Inventory',
    }
        # fetch only raw materials and send via dictionary give name>> materials
        return render(request, 'home/stock_qty_raw.html',context)

def stock_coverage(request):
    context = {
        'app_name': 'Inventory',
    }
    return render(request, 'home/stock_cvg.html',context)

def milk_procurementation(request):
    context = {
        'app_name': 'Inventory',
    }
    return render(request, 'home/milk_procurementation.html',context)

def active_sku(request):
    context = {
        'app_name': 'Inventory',
    }
    return render(request, 'home/active_sku.html',context)

def all_product_list(request):
    context = {
        'app_name': 'Inventory',
    }
    return render(request, 'home/all_product.html',context)

def inventory_value(request):
    context = {
        'app_name': 'Inventory',
    }
    return render(request, 'home/inventory_value.html',context)

def inventory_transaction_summary(request):
    context = {
        'app_name': 'Inventory',
    }
    return render(request, 'home/inventory_transaction_summary.html',context)

def stoke_movement_analysis(request):
    context = {
        'app_name': 'Inventory',
    }
    return render(request, 'home/stoke_movement_analysis.html',context)

def open_purchase_orders(request):
    context = {
        'app_name': 'Inventory',
    }
    return render(request, 'home/open_purchase_orders.html',context)

def cycle_count_stock_audit(request):
    context = {
        'app_name': 'Inventory',
    }
    return render(request, 'home/cycle_count_stock_audit.html',context)

def historic_trend_analysis(request):
    context = {
        'app_name': 'Inventory',
    }
    return render(request, 'home/historic_trend_analysis.html',context)
