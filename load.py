import json
from mongoengine import connect
from finance.models import Order  # Adjust your model import if needed


connect(
    db='Cluster0',  # Name of the database
    host='mongodb+srv://manufacturingerp:manufacturingerp@cluster0.0e3st.mongodb.net/Cluster0?retryWrites=true&w=majority&tls=true&appName=Cluster0'
)
# Load your JSON data
with open(r'C:\Users\Pinak\MCA\PythonDjango\programs\manufacturing_erp\data.json', 'r') as f:  # Use a raw string
    data = json.load(f)

# Iterate over the data and add it to the database
for item in data:
    order = Order(
        order_id=item["order_id"],
        customer_id=item["customer_id"],  # Reference to existing Customer
        sku_id=item["sku_id"],  # Reference to existing SKU
        qty=item["qty"],
        regularity=item["regularity"],
        day=item["day"]
    )
    order.save()

print("Data successfully added to the database.")
