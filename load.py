import json
from mongoengine import connect
from finance.models import Supplier  # Adjust your model import if needed


connect(
    db='Cluster0',  # Name of the database
    host='mongodb+srv://manufacturingerp:manufacturingerp@cluster0.0e3st.mongodb.net/Cluster0?retryWrites=true&w=majority&tls=true&appName=Cluster0'
)
# Load your JSON data
with open(r'C:\Users\Pinak\MCA\PythonDjango\programs\manufacturing_erp\data.json', 'r') as f:  # Use a raw string
    data = json.load(f)

# Iterate over the data and add it to the database
supplier = Supplier(
        supplier_id=9467364,
        supplier_name="Collection Center",
        supplier_contact="1234567890",
        raw_material_id=[12966],
        description="Leading supplier of raw materials."
    )
supplier.save()

print("Data successfully added to the database.")
