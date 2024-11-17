import json
from mongoengine import connect
from production.models import BOM  # Adjust your model import if needed


connect(
    db='Cluster0',  # Name of the database
    host='mongodb+srv://manufacturingerp:manufacturingerp@cluster0.0e3st.mongodb.net/Cluster0?retryWrites=true&w=majority&tls=true&appName=Cluster0'
)
# Load your JSON data
with open(r'C:\Users\Pinak\MCA\PythonDjango\programs\manufacturing_erp\data.json', 'r') as f:  # Use a raw string
    data = json.load(f)

# Iterate over the data and add it to the database
for item in data:
    b_o_m = BOM(
        bom_id=item["bom_id"],
        sku_id=item["sku_id"],  # Assuming sku_id is a single value
        raw_material_id=item["raw_material_id"],  # Directly use the list
        qty_required=item["qty_required"],  # Directly use the list of floats
        machine_required=item["machine_required"],  # Directly use the list of strings
        designation_id=item["designation_id"],  # Directly use the list of integers
        required_worker=item["required_worker"],  # Directly use the list of integers
        by_product=item["by_product"] if item["by_product"] is not None else None,  # Handle None value
        qty_to_be_produced=int(item["qty_to_be_produced"])  # Ensure it's an integer
    )
    b_o_m.save()

print("Data successfully added to the database.")
