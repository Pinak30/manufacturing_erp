from django.shortcuts import render
from .models import *
from mongoengine import Q
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
            raw_material = material.raw_material_id  # Access the referenced RawMaterial object directly

            manufacturing_date = material.manufacturing_date
            if manufacturing_date and raw_material.raw_material_life_span:
                # Calculate expiry date
                expiry_date = manufacturing_date + timedelta(days=raw_material.raw_material_life_span)

                # Calculate time remaining until expiry
                remaining_life = (expiry_date - timezone.now().date()).days
        
                # If remaining life is negative, set it to zero to indicate expiry
                if remaining_life < 0:
                    remaining_life = 0
            else:
                remaining_life = None
                expiry_date = None

            material_list.append({
                'product_name': raw_material.raw_material_name,
                'life_span': raw_material.raw_material_life_span,
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
    milk_raw_material = RawMaterial.objects(raw_material_name="milk").first()
    milk = PurchaseOrderItem.objects.filter(raw_material_id=milk_raw_material.id) if milk_raw_material else []
    context = {
        'app_name': 'Inventory',
        'milk': milk
    }
    return render(request, 'home/milk_procurementation.html', context)


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
    # Calculate total inventory value for finished products
    finished_product_value = ProductInventory.objects.aggregate(
        {
            '$lookup': {
                'from': 'sku',
                'localField': 'sku_id',
                'foreignField': '_id',
                'as': 'sku_info'
            }
        },
        {
            '$unwind': '$sku_info'
        },
        {
            '$project': {
                'total_value': {'$multiply': ['$quantity', '$sku_info.unit_price']}
            }
        },
        {
            '$group': {
                '_id': None,
                'total_value': {'$sum': '$total_value'}
            }
        }
    )
    finished_product_value = list(finished_product_value)
    finished_product_value = finished_product_value[0]['total_value'] if finished_product_value else 0

    # Calculate total inventory value for raw materials
    raw_material_value = InventoryRawMaterial.objects.aggregate(
        {
            '$lookup': {
                'from': 'raw_material',
                'localField': 'raw_material_id',
                'foreignField': '_id',
                'as': 'raw_material_info'
            }
        },
        {
            '$unwind': '$raw_material_info'
        },
        {
            '$project': {
                'total_value': {'$multiply': ['$quantity_in_stock', '$raw_material_info.raw_material_unit_price']}
            }
        },
        {
            '$group': {
                '_id': None,
                'total_value': {'$sum': '$total_value'}
            }
        }
    )
    raw_material_value = list(raw_material_value)
    raw_material_value = raw_material_value[0]['total_value'] if raw_material_value else 0

    # Calculate total inventory value (finished products + raw materials)
    total_inventory_value = finished_product_value + raw_material_value

    # Fetch the list of SKUs and their inventory values
    sku_inventory_values = ProductInventory.objects.aggregate(
        {
            '$lookup': {
                'from': 'sku',
                'localField': 'sku_id',
                'foreignField': '_id',
                'as': 'sku_info'
            }
        },
        {
            '$unwind': '$sku_info'
        },
        {
            '$project': {
                'sku_name': '$sku_info.sku_name',
                'total_value': {'$multiply': ['$quantity', '$sku_info.unit_price']}
            }
        }
    )
    sku_inventory_values = list(sku_inventory_values)

    context = {
        'app_name': 'Inventory',
        'total_inventory_value': total_inventory_value,
        'raw_material_value': raw_material_value,
        'finished_product_value': finished_product_value,
        'sku_inventory_values': sku_inventory_values,
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
