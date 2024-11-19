from django.shortcuts import render, redirect
from .models import *
from finance.models import *
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.utils.timezone import now
import re

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


def purchase_order(request):
    # Fetch all raw materials
    raw_materials = RawMaterial.objects.all()
    suppliers = []
    selected_raw_material = None
    selected_supplier = None
    entered_quantity = 0
    entered_unit_price = 0  
    entered_order_date = ""
    entered_delivery_date = ""
    total_amount = 0  # Variable to hold total amount

    # Fetch the last purchase order and purchase order finance to continue the purchase_order_id from 9797
    last_purchase_order_finance = PurchaseOrderFinance.objects.order_by('-purchase_order_id').first()
    next_purchase_order_id = 9797 if not last_purchase_order_finance else last_purchase_order_finance.purchase_order_id + 1

    # Fetch the last purchase order item to continue the purchase_order_item_id from 1550
    last_purchase_order_item = PurchaseOrderItem.objects.order_by('-purchase_order_item_id').first()
    next_purchase_order_item_id = 1550 if not last_purchase_order_item else last_purchase_order_item.purchase_order_item_id + 1

    # Fetch the last expense to continue the expense_id from 1e642681
    last_expense = Expense.objects.order_by('-expense_id').first()
    next_expense_id = '1e642681' if not last_expense else hex(int(last_expense.expense_id, 16) + 1)[2:]

    # Fetch the last transaction ID for Transaction
    last_transaction = Transaction.objects.order_by('-transaction_id').first()
    next_transaction_id = '5a1332' if not last_transaction else hex(int(last_transaction.transaction_id, 16) + 1)[2:]

    if request.method == 'POST':
        # Get the selected raw material and supplier from the form submission
        selected_raw_material_id = request.POST.get('raw_material_id')
        selected_supplier_id = request.POST.get('supplier_id')
        entered_quantity = request.POST.get('quantity', 0)
        entered_unit_price = request.POST.get('unit_price', 0)  
        entered_order_date = request.POST.get('order_date', "")
        entered_delivery_date = request.POST.get('delivery_date', "")

        # Fetch the selected raw material and suppliers based on the raw material
        if selected_raw_material_id:
            selected_raw_material = RawMaterial.objects.get(raw_material_id=selected_raw_material_id)
            # Fetch the suppliers for the selected raw material
            suppliers = Supplier.objects.filter(raw_material_id=selected_raw_material)

        if selected_supplier_id:
            selected_supplier = Supplier.objects.get(supplier_id=selected_supplier_id)

        # Calculate total amount based on selected quantity and raw material price
        if entered_quantity and entered_unit_price:
            total_amount = float(entered_quantity) * float(entered_unit_price)

            # Create the PurchaseOrderFinance object
            purchase_order_finance = PurchaseOrderFinance.objects.create(
                purchase_order_id=next_purchase_order_id,
                order_date=datetime.strptime(entered_order_date, '%Y-%m-%d'),
                supplier_id=selected_supplier,
                total_amount=total_amount,
                expected_delivery_date=datetime.strptime(entered_delivery_date, '%Y-%m-%d'),
            )
            purchase_order_finance.save()

            # Create the PurchaseOrder object (same purchase_order_id as PurchaseOrderFinance)
            purchase_order = PurchaseOrder.objects.create(
                purchase_order_id=next_purchase_order_id,
                supplier_id=selected_supplier.supplier_id,
                order_date=datetime.strptime(entered_order_date, '%Y-%m-%d'),
            )
            purchase_order.save()

            # Create the PurchaseOrderItem entry for the raw material
            purchase_order_item = PurchaseOrderItem.objects.create(
                purchase_order_item_id=next_purchase_order_item_id,
                purchase_order_id=purchase_order,
                raw_material_id=selected_raw_material,
                quantity=entered_quantity,
                price_per_unit=entered_unit_price,
            )
            purchase_order_item.save()

            # Create the Expense entry with expense_type as "Inventory"
            expense = Expense.objects.create(
                expense_id=next_expense_id,
                expense_type="inventory",
                amount=total_amount,
                purchase_order_id=purchase_order_finance,
            )
            expense.save()

            # Update Account balances
            debit_account = Account.objects.get(account_id=462346553)
            credit_account = Account.objects.get(account_id=493446675)

            debit_account.balance += total_amount
            credit_account.balance -= total_amount

            debit_account.save()
            credit_account.save()

            # Update General Ledger closing balances
            ledger_118 = GeneralLedger.objects.get(ledger_id="23LED118a")
            ledger_120 = GeneralLedger.objects.get(ledger_id="23LED120")

            ledger_118.closing_balance -= total_amount
            ledger_120.closing_balance -= total_amount

            ledger_118.save()
            ledger_120.save()

            # Create the Transaction entry
            transaction = Transaction.objects.create(
                transaction_id=next_transaction_id,
                transaction_date=datetime.strptime(entered_order_date, '%Y-%m-%d'),
                amount=total_amount,
                account_id=credit_account,
                ledger_id=ledger_120,
                payment_id=None,  # Payment ID is null
                expense_id=expense,
            )
            transaction.save()

            # Redirect to a success page or pass success message
            return render(request, 'home/purchase_order_success.html', {'purchase_order': purchase_order})

    # Default context when the form has not been submitted yet
    context = {
        'raw_materials': raw_materials,
        'suppliers': suppliers,
        'selected_raw_material': selected_raw_material,
        'selected_supplier': selected_supplier,
        'entered_quantity': entered_quantity,
        'entered_order_date': entered_order_date,
        'entered_delivery_date': entered_delivery_date,
        'entered_unit_price': entered_unit_price,
        'total_amount': total_amount,
        'app_name': 'Inventory',
    }

    return render(request, 'home/purchase_order.html', context)


def purchase_order_list(request):
    # Fetch all purchase orders from PurchaseOrderFinance
    purchase_orders = PurchaseOrderFinance.objects.all()

    # Fetch the last inventory ID for InventoryRawMaterial
    last_inventory = InventoryRawMaterial.objects.order_by('-inventory_id').first()
    next_inventory_id = 44525 if not last_inventory else last_inventory.inventory_id + 1

    if request.method == 'POST':
        # Handle the "Delivered" button action
        purchase_order_id = request.POST.get('purchase_order_id')

        # Fetch the purchase order
        purchase_order = PurchaseOrderFinance.objects.filter(purchase_order_id=purchase_order_id).first()
        if purchase_order:
            # Check if the expected delivery date is today or in the past
            if purchase_order.expected_delivery_date <= now().date():
                # Fetch the related PurchaseOrderItem based on the foreign key
                purchase_order_item = PurchaseOrderItem.objects.filter(purchase_order_id=purchase_order_id).first()

                if purchase_order_item:
                    # Add the raw material from PurchaseOrderItem to the inventory
                    InventoryRawMaterial.objects.create(
                        inventory_id=next_inventory_id,
                        raw_material_id=purchase_order_item.raw_material_id,
                        quantity_in_stock=purchase_order_item.quantity,  # Get quantity from the matched item
                        location=None,  # Example location
                        manufacturing_date=purchase_order.order_date,  # Leave empty if not provided
                        order_date=purchase_order.order_date,
                    )
                    next_inventory_id += 1

                    # Mark the purchase order as delivered (optional: add a delivered flag in PurchaseOrderFinance)
                    purchase_order.delivered = True
                    purchase_order.save()

        # Redirect to refresh the page
        return redirect('orders_lists')  # Use the URL name of this view

    # Pass the purchase orders to the template
    context = {
        'purchase_orders': purchase_orders,
        'app_name': 'Inventory',
    }

    return render(request, 'home/purchase_order_list.html', context)


def increment_id(current_id):
    """
    Increment the numeric portion at the end of an alphanumeric ID.

    Args:
        current_id (str): The current ID to increment.

    Returns:
        str: The incremented ID.
    """
    # Find the last sequence of digits in the ID
    match = re.search(r'(\d+)(?!.*\d)', current_id)
    if match:
        # Extract the numeric part and increment it
        numeric_part = match.group(1)
        incremented_part = str(int(numeric_part) + 1)

        # Pad with leading zeros to match the original length
        incremented_part = incremented_part.zfill(len(numeric_part))

        # Replace the old numeric part with the incremented part
        return current_id[:match.start()] + incremented_part + current_id[match.end():]
    else:
        # If no numeric part is found, return the original ID
        return current_id


def order_list_view(request):
    # Fetch all orders
    orders = Order.objects.all()

    # Fetch the last IDs for Invoice, Payment, and Transaction
    last_invoice = Invoice.objects.order_by('-invoice_id').first()
    next_invoice_id = increment_id("1a2341b289") if not last_invoice else increment_id(last_invoice.invoice_id)

    last_payment = Payment.objects.order_by('-payment_id').first()
    next_payment_id = increment_id("1c345v692") if not last_payment else increment_id(last_payment.payment_id)

    last_transaction = Transaction.objects.order_by('-transaction_id').first()
    next_transaction_id = increment_id("5a1344") if not last_transaction else increment_id(last_transaction.transaction_id)

    if request.method == 'POST':
        # Handle the "Done" button
        order_id = request.POST.get('order_id')
        order = Order.objects.filter(order_id=order_id).first()

        if order:
            # Get related details
            customer = order.customer_id
            sku = order.sku_id
            raw_material = RawMaterial.objects.filter(raw_material_id=sku.sku_id).first()

            if raw_material:
                unit_price = raw_material.raw_material_unit_price
                total_amount = order.qty * unit_price

                # Create Invoice entry
                invoice = Invoice.objects.create(
                    invoice_id=next_invoice_id,
                    invoice_date=datetime.now().date(),
                    customer_id=customer,
                    amount=total_amount
                )

                # Create Payment entry
                payment = Payment.objects.create(
                    payment_id=next_payment_id,
                    payment_date=datetime.now().date(),
                    amount_paid=total_amount,
                    invoice_id=invoice
                )

                # Update the Account balance (for account ID `493446675`)
                account = Account.objects.filter(account_id=493446675).first()
                if account:
                    account.balance += total_amount
                    account.save()

                # Update General Ledger balances
                ledger_120 = GeneralLedger.objects.filter(ledger_id="23LED120").first()
                if ledger_120:
                    ledger_120.closing_balance += total_amount
                    ledger_120.save()

                ledger_118 = GeneralLedger.objects.filter(ledger_id="23LED118").first()
                if ledger_118:
                    ledger_118.closing_balance += total_amount
                    ledger_118.save()

                # Create Transaction entry
                Transaction.objects.create(
                    transaction_id=next_transaction_id,
                    transaction_date=datetime.now().date(),
                    amount=total_amount,
                    account_id=account,
                    ledger_id=ledger_120,  # Assuming ledger ID is 23LED120 for this transaction
                    payment_id=payment,
                    expense_id=None  # Set to None if expense_id is not provided
                )

        # Redirect to refresh the page
        return redirect('order_list')

    # Pass orders to the template
    context = {
        'orders': orders,
        'app_name': 'Inventory',
    }
    return render(request, 'home/daily_order.html', context)


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
