import json
from inventory.models import *
from datetime import datetime

# Load your JSON data
with open(r'C:\Users\Pinak\OneDrive\Desktop\SKU (1).json', 'r') as f:  # Use a raw string
    data = json.load(f)# Access the relevant key if it's still part of the data structure

# Iterate over the data and add it to the database
for item in data:
    product_inventory = ProductInventory(
        product_inventory_id=item["product_inventory_id"],
        sku_id=item.get("sku_id") or None,  # Handle null
        quantity=item.get("quantity") or 0,  # Default to 0 if null
        location=item.get("location") or '',  # Default to empty string if null
        manufacturing_date=item.get("manufacturing_date") or None,  # Handle null
        expiry_date=item.get("expiry_date") or None  # Handle null
    )
    product_inventory.save()

print("Data successfully added to the database.")
