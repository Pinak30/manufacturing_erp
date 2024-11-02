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

    # Calculate remaining life for raw materials
    material_list = []
    for material in materials:
        if material.raw_material_id:
            raw_material = RawMaterial.objects.get(raw_material_id=material.raw_material_id.raw_material_id)
            manufacturing_date = material.manufacturing_date

            if manufacturing_date:
                # Calculate time passed since manufacturing
                time_passed = (timezone.now().date() - manufacturing_date).days
                remaining_life = raw_material.raw_material_life_span - time_passed if raw_material.raw_material_life_span is not None else None
                
                # If remaining life is negative, set it to zero
                if remaining_life is not None and remaining_life < 0:
                    remaining_life = 0  # Indicates the material has expired

                # Calculate expiry date
                expiry_date = manufacturing_date + timedelta(days=raw_material.raw_material_life_span) if raw_material.raw_material_life_span is not None else None
            else:
                remaining_life = None
                expiry_date = None
            
            material_list.append({
                'product_name': raw_material.raw_material_name if raw_material else 'Unknown',
                'life_span': raw_material.raw_material_life_span if raw_material else 'N/A',
                'remaining_life': remaining_life,
                'expiry_date': expiry_date,
            })

    # Calculate remaining life for ready products
    product_list = []
    for product in products:
        if product.expiry_date:
            # Calculate remaining days until expiry date
            remaining_life = (product.expiry_date - timezone.now().date()).days
            if remaining_life < 0:
                remaining_life = 0  # Indicates the product has expired
        else:
            remaining_life = "No expiry date available"

        product_list.append({
            'product_name': product.sku_id.sku_name,  # Assuming sku_id relates to product name
            'quantity': product.quantity,
            'expiry_date': product.expiry_date,
            'remaining_life': remaining_life,
        })

    context = {
        'app_name': 'Inventory',
        'products': product_list,  # Updated to use product_list with remaining life info
        'materials': material_list,
    }

    return render(request, 'home/stock_cvg.html', context)


def milk_procurementation(request):
    milk = PurchaseOrderItem.objects.all()
    # milk = PurchaseOrderItem.objects.filter(raw_material_id__raw_material_name="milk")
    context = {
        'app_name': 'Inventory',
        'milk':milk
    }
    return render(request, 'home/milk_procurementation.html',context)

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

def stoke_movement_analysis(request):
    context = {
        'app_name': 'Inventory',
    }
    return render(request, 'home/stoke_movement_analysis.html',context)

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
