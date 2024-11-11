from django.shortcuts import render
from .models import *
from inventory.models import InventoryRawMaterial

# Create your views here.

def production(request):
        context = {
        'app_name': 'Production',  # Pass app name dynamically
    }
        return render(request, 'home/production.html',context)

def masterproduction(request):
    bom_list = BOM.objects.all()
    selected_sku_id = request.GET.get("sku_id")
    entered_quantity = request.GET.get("quantity", 0)

    selected_bom = None
    raw_materials_info = []
    batches_info = {}

    if selected_sku_id and entered_quantity:
        selected_bom = BOM.objects.filter(sku_id=selected_sku_id).first()
        if selected_bom:
            entered_quantity = int(entered_quantity)

            # Table data: fetching actual quantity from InventoryRawMaterial and required quantity from BOM
            for index, raw_material in enumerate(selected_bom.raw_material_id):
                # Fetch InventoryRawMaterial instance for actual quantity in stock
                inventory_item = InventoryRawMaterial.objects.filter(raw_material_id=raw_material).first()
                actual_qty = inventory_item.quantity_in_stock if inventory_item else 0
                
                # Required quantity for the specific raw material (directly from BOM's qty_required list)
                required_qty = selected_bom.qty_required[index]
                
                raw_materials_info.append({
                    "name": raw_material.raw_material_name,
                    "actual_qty": actual_qty,
                    "required_qty": required_qty,
                    "needs_reorder": actual_qty < required_qty,
                })

            # After the table, calculate the batch distribution based on entered_quantity
            quantity_to_be_produced = selected_bom.qty_to_be_produced
            full_batches = entered_quantity // quantity_to_be_produced
            remainder = entered_quantity % quantity_to_be_produced
            batches_info = {
                "batch_size": quantity_to_be_produced,
                "batches_required": full_batches + (1 if remainder else 0),
                "batch_distribution": [quantity_to_be_produced] * full_batches + ([remainder] if remainder else [])
            }

    context = {
        'app_name': 'Production',
        'bom_list': bom_list,
        'selected_bom': selected_bom,
        'raw_materials_info': raw_materials_info,
        'selected_sku_id': selected_sku_id,
        'entered_quantity': entered_quantity,
        'batches_info': batches_info
    }
    return render(request, 'home/masterproduction.html', context)

def bommanagement(request):
        bom = BOM.objects.all()
        context = {
        'app_name': 'Production',  # Pass app name dynamically
        'bom': bom,
    }
        return render(request, 'home/bommanagement.html',context)


def materialreqplan(request):
        context = {
        'app_name': 'Production',  # Pass app name dynamically
    }
        return render(request, 'home/materialreqplan.html',context)


def workordermanage(request):
        context = {
        'app_name': 'Production',  # Pass app name dynamically
    }
        return render(request, 'home/workordermanage.html',context)