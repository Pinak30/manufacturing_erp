from django.shortcuts import render, redirect, get_object_or_404
from .forms import BOMForm
from .models import *
from inventory.models import InventoryRawMaterial
from authentication.models import Employee
from django.contrib import messages
from django.http import JsonResponse
from datetime import date
import re


# Create your views here.
def production(request):
        context = {
        'app_name': 'Production',  # Pass app name dynamically
    }
        return render(request, 'home/production.html',context)

# Helper function to get the next assignment_id
# def get_next_assignment_id():
#     from django.db.models import Max
#     last_assignment = ProductionShiftAssignments.objects.aggregate(Max('_id'))
#     return (last_assignment['_id__max'] or 0) + 1

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
        # Fetch the last plan_id, ordered by descending order
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
    entered_quantity = request.GET.get("quantity", 0)

    # Automatically generate producrtion_order_id
    production_order_id = generate_production_order_id()
    # Insert in production_order
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
    assignments = []  # Initialize assignments as an empty list

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
                "batch_distribution": [quantity_to_be_produced] * full_batches + ([remainder] if remainder else []),
            }
            
            # Automatically generate plan_id
            plan_id = generate_plan_id()
            # Insert in plan_production
            PlanProduction.objects.create(
                plan_id=plan_id,
                production_order_id=production_order_id,
                bom_id=selected_bom.bom_id,
                batch_design=[quantity_to_be_produced] * full_batches + ([remainder] if remainder else []),
                no_of_batches=full_batches + (1 if remainder else 0),
                reorder_status=1,
                status=1,
            )

            # Work shift assignment (simplified)
            try:
                # Loop through each designation and its required workers
                for index, designation_id in enumerate(selected_bom.designation_id):
                    required_workers = selected_bom.required_worker[index]
                    
                    # Fetch employees with matching designation_id (no check for already assigned employees)
                    available_employees = Employee.objects.filter(
                        designation_id=designation_id
                    )[:required_workers]  # Ensure we only fetch the required number of employees
                    
                    # Loop through the selected employees and assign them to shifts
                    for employee in available_employees:
                        shift_timing = employee.shift_timings.lower()
                        try:
                            # Match shift_type in WorkShift to the employee's shift_timing
                            work_shift = WorkShift.objects.get(shift_type=shift_timing)

                            # Generate the next assignment ID
                            next_assignment_id = 13335535

                            # Create the ProductionShiftAssignments entry
                            # ProductionShiftAssignments.objects.create(
                            #     _id=next_assignment_id,
                            #     shift_id=work_shift,
                            #     employee_id=employee,
                            #     date_assigned=date.today()
                            # )

                            # Add the assignment to the list
                            assignments.append({
                                "_id": next_assignment_id,
                                "employee_name": employee.employee_name,
                                "designation_id": designation_id,
                                "shift_type": shift_timing,
                                "date_assigned":date.today()
                            })
                            next_assignment_id+1
                        except WorkShift.DoesNotExist:
                            return JsonResponse({"error": f"No work shift found for timing: {shift_timing}"}, status=404)

                # Return the response with assignments included in the context
                context = {
                    'app_name': 'Production',
                    'bom_list': bom_list,
                    'selected_bom': selected_bom,
                    'raw_materials_info': raw_materials_info,
                    'selected_sku_id': selected_sku_id,
                    'entered_quantity': entered_quantity,
                    'batches_info': batches_info,
                    'assignments': assignments,  # Pass assignments here
                }
                return render(request, 'home/masterproduction.html', context)

            except BOM.DoesNotExist:
                return JsonResponse({"error": "BOM not found"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

    # Default context if no SKU is selected or no quantity is entered
    context = {
        'app_name': 'Production',
        'bom_list': bom_list,
        'selected_bom': selected_bom,
        'raw_materials_info': raw_materials_info,
        'selected_sku_id': selected_sku_id,
        'entered_quantity': entered_quantity,
        'batches_info': batches_info,
        'assignments': assignments,  # Ensure assignments is included in context
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