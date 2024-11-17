from django.shortcuts import render, redirect, get_object_or_404
from .forms import BOMForm
from .models import *
from inventory.models import InventoryRawMaterial
from django.contrib import messages

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
    """
    List all BOMs with basic details.
    """
    bom = BOM.objects.all()
    context = {
        'app_name': 'Production',
        'bom': bom,
    }
    return render(request, 'home/bommanagement.html', context)


def bom_add(request):
    """
    View for adding a new BOM.
    """
    if request.method == 'POST':
        form = BOMForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "BOM created successfully!")
            return redirect('bommanagement')  # Redirect to BOM management page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BOMForm()

    context = {
        'app_name': 'Production',
        'segment': 'create_bom',
        'form': form,
        'is_update': False,
    }
    return render(request, 'home/bomadd.html', context)


def bom_update(request, bom_id):
    """
    View for updating an existing BOM.
    """
    try:
        bom = BOM.objects.get(bom_id=bom_id)
    except BOM.DoesNotExist:
        messages.error(request, "The book you're trying to edit does not exist.")
        return redirect('book_list')

    if request.method == 'POST':
        form = BOMForm(request.POST)
        if form.is_valid():
            form.save(instance=bom)
            messages.success(request, "BOM updated successfully!")
            return redirect('viewbom', bom_id=bom.bom_id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BOMForm(initial={
            'bom_id': bom.bom_id,
            'sku_id': str(bom.sku_id),
            'raw_material_id': [str(rm) for rm in bom.raw_material_id],
            'qty_required': ','.join(map(str, bom.qty_required)),
            'machine_required': ','.join(bom.machine_required),
            'designation_id': [str(des) for des in bom.designation_id],
            'required_worker': ','.join(map(str, bom.required_worker)),
            'by_product': ','.join(map(str, bom.by_product)),
            'qty_to_be_produced': bom.qty_to_be_produced,
        })

    context = {
        'app_name': 'Production',
        'segment': 'update_bom',
        'form': form,
        'is_update': True,
    }
    return render(request, 'home/bomadd.html', context)


def viewbom(request, bom_id):
    """
    View detailed BOM information.
    """
    try:
        bom = BOM.objects.get(bom_id=bom_id)
    except BOM.DoesNotExist:
        return redirect('bommanagement')

    raw_materials = []
    for i in range(len(bom.raw_material_id)):
        # Fetch the Designation object
        rawMaterial_obj = bom.raw_material_id[i] # Assuming Designation is referenced by _id or id
        count = bom.qty_required[i]
        raw_materials.append((rawMaterial_obj.raw_material_name, count))

    # Zip designation_id and required_worker together
    designation_worker_details = []
    for i in range(len(bom.designation_id)):
        # Fetch the Designation object
        designation_obj = bom.designation_id[i] # Assuming Designation is referenced by _id or id
        worker = bom.required_worker[i]
        designation_worker_details.append((designation_obj.designation_name, worker))

    context = {
        'bom': bom,
        'raw_materials': raw_materials,
        'designation_worker_details': designation_worker_details,  
        'app_name': 'Production', 
    }

    return render(request, 'home/viewbom.html', context)


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