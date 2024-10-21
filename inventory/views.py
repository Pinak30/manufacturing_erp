from django.shortcuts import render
from .models import *
from django.utils import timezone
from datetime import timedelta
from datetime import date

# Create your views here.
def inventory(request):
    context = {
        'app_name': 'Inventory',
    }
    return render(request, 'home/inventory.html',context)

from inventory.models import ProductInventory

def stock_qty(request):
    products = ProductInventory.objects.all()  # Fetch all product inventories
    context = {
        'app_name': 'Inventory',
        'products': products,
    }
    return render(request, 'home/stock_qty.html', context)


def stock_qty_raw(request):
    materials = InventoryRawMaterial.objects.all()
    context = {
        'app_name': 'Inventory',
        'materials': materials,
    }
    return render(request, 'home/stock_qty_raw.html',context)

def stock_coverage(request):
    products = ProductInventory.objects.all()
    materials = InventoryRawMaterial.objects.all()

    for product in products:
        if product.expiry_date:
            # Calculate remaining days from expiry_date
            product.remaining_life = (product.expiry_date - date.today()).days
        else:
            product.remaining_life = "No expiry date available"

    material_list = []
    for material in materials:
        if material.raw_material_id:
            raw_material = RawMaterial.objects.get(raw_material_id=material.raw_material_id.raw_material_id)  # Get the corresponding raw material's life span
            manufacturing_date = material.manufacturing_date  # Calculate the time passed since the manufacturing date

            if manufacturing_date:
                time_passed = (timezone.now().date() - manufacturing_date).days

                # Check if raw_material_life_span is not None
                if raw_material.raw_material_life_span is not None:
                    remaining_life = raw_material.raw_material_life_span - time_passed
                else:
                    remaining_life = None  # Set to None if life span is not available

                if remaining_life is not None and remaining_life < 0:
                    remaining_life = 0  # if expired
                
                # Calculate the expiry date
                expiry_date = manufacturing_date + timedelta(days=raw_material.raw_material_life_span) if raw_material.raw_material_life_span is not None else None

            else:
                remaining_life = None  # Set to None if no manufacturing date
                expiry_date = None
            
            # Append the data to the list with calculated fields
            material_list.append({
                'product_name': raw_material.raw_material_name if raw_material else 'Unknown',
                'life_span': raw_material.raw_material_life_span if raw_material else 'N/A',
                'remaining_life': remaining_life,
                'expiry_date': expiry_date,
            })
        else:
            # Handle cases where raw_material_id is None
            material_list.append({
                'product_name': 'Unknown',
                'life_span': 'N/A',
                'remaining_life': None,  # Set to None
                'expiry_date': None,
            })

    context = {
        'app_name': 'Inventory',
        'products': products,
        'materials': material_list,  # Pass the updated material list with remaining life
    }

    return render(request, 'home/stock_cvg.html', context)


# def milk_procurementation(request):
#     milk = PurchaseOrderItem.objects.all()
#     # milk = PurchaseOrderItem.objects.filter(raw_material_id__raw_material_name="milk")
#     context = {
#         'app_name': 'Inventory',
#         'milk':milk
#     }
#     return render(request, 'home/milk_procurementation.html',context)

def active_sku(request):
    sku = Sku.objects.filter(active=2)
    context = {
        'app_name': 'Inventory',
        'sku' : sku,
    }
    return render(request, 'home/active_sku.html',context)

def all_product_list(request):
    sku = Sku.objects.all()
    context = {
        'app_name': 'Inventory',
        'sku' : sku,
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

# def stoke_movement_analysis(request):
#     context = {
#         'app_name': 'Inventory',
#     }
#     return render(request, 'home/stoke_movement_analysis.html',context)

# def open_purchase_orders(request):
#     context = {
#         'app_name': 'Inventory',
#     }
#     return render(request, 'home/open_purchase_orders.html',context)

# def cycle_count_stock_audit(request):
#     context = {
#         'app_name': 'Inventory',
#     }
#     return render(request, 'home/cycle_count_stock_audit.html',context)

# def historic_trend_analysis(request):
#     context = {
#         'app_name': 'Inventory',
#     }
#     return render(request, 'home/historic_trend_analysis.html',context)
