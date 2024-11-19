from django.shortcuts import render, redirect, get_object_or_404
from .forms import BOMForm
from .models import *
from inventory.models import InventoryRawMaterial, RawMaterial
from authentication.models import Employee
from django.contrib import messages
from django.http import JsonResponse
from datetime import date, datetime
import re


# Create your views here.
def production(request):
        context = {
        'app_name': 'Production',  # Pass app name dynamically
    }
        return render(request, 'home/production.html',context)

def get_next_assignment_id():
    try:
        last_assignment_id = ProductionShiftAssignments.objects.order_by('-assignment_id').first()
        if last_assignment_id:
            last_id = last_assignment_id.assignment_id
            new_id = f"{last_id + 1:05d}"
        else:
            new_id = f"00000001"
    except last_assignment_id.DoesNotExist:
        new_id = f"00000001"
    return new_id

def generate_production_order_id():
    try:
        last_prod_order_id = ProductionOrder.objects.order_by('-production_order_id').first()
        if last_prod_order_id:
            last_id = last_prod_order_id.production_order_id
            new_id = f"{last_id + 1:05d}"
        else:
            new_id = f"00000000000001"
    except last_prod_order_id.DoesNotExist:
        new_id = f"00000000000001"
    return new_id

def generate_plan_id():
    prefix = "la"
    try:
        last_plan_id = PlanProduction.objects.order_by('-plan_id').first()
        
        if last_plan_id:
            last_id_str = last_plan_id.plan_id.replace(prefix, "")  # Remove prefix 'la'
            numeric_part = re.sub(r'\D', '', last_id_str)  # \D matches anything that is not a digit
            last_id = int(numeric_part) if numeric_part else 0
            new_id = f"{prefix}{last_id + 1:011d}"  # Adjust padding as needed
        else:
            new_id = f"{prefix}00000000001"  # Start from this if no records exist
    except Exception as e:
        new_id = f"{prefix}00000000001"  # In case of any error, start from this
        print(f"Error in generating plan_id: {e}")
    
    return new_id

def masterproduction(request):
    bom_list = BOM.objects.all()
    selected_sku_id = request.GET.get("sku_id")
    entered_quantity = int(request.GET.get("quantity", 0))  # Ensure integer conversion

    # Automatically generate production_order_id
    production_order_id = str(generate_production_order_id())  # Convert to string if needed
    ProductionOrder.objects.create(
        production_order_id=production_order_id,
        sku_id=selected_sku_id,
        order_date=date.today(),
        planned_quantity=entered_quantity,
        status=1
    )

    selected_bom = None
    raw_materials_info = []
    batches_info = {}
    assignments = []

    if selected_sku_id and entered_quantity:
        selected_bom = BOM.objects.filter(sku_id=selected_sku_id).first()
        if selected_bom:
            entered_quantity = int(entered_quantity)

            for index, raw_material in enumerate(selected_bom.raw_material_id):
                inventory_item = InventoryRawMaterial.objects.filter(raw_material_id=raw_material).first()
                actual_qty = inventory_item.quantity_in_stock if inventory_item else 0
                required_qty = selected_bom.qty_required[index]
                quantity_to_be_produced = selected_bom.qty_to_be_produced
                qty = entered_quantity // quantity_to_be_produced

                raw_materials_info.append({
                    "name": raw_material.raw_material_name,  # Ensure this is a string
                    "actual_qty": actual_qty,
                    "required_qty": required_qty * qty,
                    "needs_reorder": actual_qty < required_qty,
                })

            full_batches = entered_quantity // quantity_to_be_produced
            remainder = entered_quantity % quantity_to_be_produced
            batches_info = {
                "batch_size": quantity_to_be_produced,
                "batches_required": full_batches + (1 if remainder else 0),
                "batch_distribution": [quantity_to_be_produced] * full_batches + ([remainder] if remainder else []),
            }

            plan_id = str(generate_plan_id())  # Convert to string if needed
            PlanProduction.objects.create(
                plan_id=plan_id,
                production_order_id=production_order_id,
                bom_id=selected_bom.bom_id,
                batch_design=[quantity_to_be_produced] * full_batches + ([remainder] if remainder else []),
                no_of_batches=full_batches + (1 if remainder else 0),
                reorder_status=1,
                status=1,
            )

            # Work shift assignment
            try:
                for index, designation_id in enumerate(selected_bom.designation_id):
                    required_workers = selected_bom.required_worker[index]
                    available_employees = Employee.objects.filter(designation_id=designation_id)[:required_workers]

                    for employee in available_employees:
                        shift_timing = employee.shift_timings.lower()
                        # work_shift = WorkShift.objects.get(shift_type=shift_timing)
                        next_assignment_id = get_next_assignment_id()

                        # ProductionShiftAssignments.objects.create(
                        #     assignment_id=next_assignment_id,
                        #     shift_id=work_shift.shift_id,
                        #     employee_id=employee.employee_id,
                        #     date_assigned=date.today()
                        # )

                        assignments.append({
                            "assignment_id": str(next_assignment_id),
                            "employee_name": employee.employee_name,
                            "designation_id": designation_id,
                            "shift_type": shift_timing,
                            "date_assigned": date.today()
                        })

                context = {
                    'app_name': 'Production',
                    'bom_list': bom_list,
                    'selected_bom': selected_bom,
                    'raw_materials_info': raw_materials_info,
                    'selected_sku_id': selected_sku_id,
                    'entered_quantity': entered_quantity,
                    'batches_info': batches_info,
                    'assignments': assignments,
                }
                return render(request, 'home/masterproduction.html', context)

            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

    context = {
        'app_name': 'Production',
        'bom_list': bom_list,
        'selected_bom': selected_bom,
        'raw_materials_info': raw_materials_info,
        'selected_sku_id': selected_sku_id,
        'entered_quantity': entered_quantity,
        'batches_info': batches_info,
        'assignments': assignments,
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
    data = []

    plan_productions = PlanProduction.objects.all()

    for plan in plan_productions:
        bom = plan.bom_id
        sku = bom.sku_id
        production_order = plan.production_order_id

        # Build data for the table
        if bom and sku and production_order:
            data.append({
                'product_name': sku.sku_name,
                'quantity': production_order.planned_quantity,
                'order_date': production_order.order_date.strftime('%d/%m/%Y'),
                'plan_id': plan.plan_id
            })
    context = {
        'app_name': 'Production',  # Pass app name dynamically
        'data': data,  # Include table data
    }
    return render(request, 'home/materialreqplan.html', context)


def batchview(request, plan_id):
    # Fetch the selected plan production and BOM
    plan_production = PlanProduction.objects.get(plan_id=plan_id)
    bom = plan_production.bom_id
    raw_materials_info = []
    batches_info = []

    # Retrieve BOM and related details
    planned_quantity = plan_production.production_order_id.planned_quantity
    qty_to_be_produced = bom.qty_to_be_produced
    full_batches = planned_quantity // qty_to_be_produced
    remainder = planned_quantity % qty_to_be_produced
    batch_distribution = [qty_to_be_produced] * full_batches + ([remainder] if remainder else [])

    # Process each batch
    for batch_index, batch_qty in enumerate(batch_distribution, start=1):
        batch_data = []
        for index, raw_material in enumerate(bom.raw_material_id):
            inventory_item = InventoryRawMaterial.objects.filter(raw_material_id=raw_material).first()
            actual_qty = inventory_item.quantity_in_stock if inventory_item else 0
            required_qty = batch_qty * bom.qty_required[index] // qty_to_be_produced

            # Adjust actual quantity based on previous batches
            if batch_index > 1:
                previous_batches_qty = sum(batch_distribution[:batch_index - 1]) * bom.qty_required[index] // qty_to_be_produced
                actual_qty -= previous_batches_qty

            needs_reorder = actual_qty < required_qty

            batch_data.append({
                "raw_material_name": raw_material.raw_material_name,
                "actual_quantity": actual_qty,
                "required_quantity": required_qty,
                "needs_reorder": needs_reorder,
            })

        batches_info.append({
            "batch_number": batch_index,
            "batch_quantity": batch_qty,
            "materials": batch_data,
        })

    context = {
        'app_name': 'Production',
        'plan_production': plan_production,
        'batches_info': batches_info,
    }

    return render(request, 'home/batchview.html', context)


def calculate_actual_quantity(batch_num, material, inventory_data, material_qty_required):
    # Calculate actual quantity considering previous batches' consumption
    actual_quantity = inventory_data[material.id][0].quantity_in_stock
    for i in range(1, batch_num):
        actual_quantity -= material_qty_required
    return actual_quantity

def deleteplan(request, plan_id):
    # Try to fetch and delete the plan production
    try:
        plan_production = PlanProduction.objects.get(plan_id=plan_id)
        plan_production.delete()
        messages.success(request, f"Plan with ID {plan_id} has been successfully deleted.")
    except PlanProduction.DoesNotExist:
        messages.error(request, f"Plan with ID {plan_id} does not exist.")
    
    return redirect('materialreqplan')

def workordermanage(request):
        context = {
        'app_name': 'Production',  # Pass app name dynamically
    }
        return render(request, 'home/workordermanage.html',context)