import json
from production.models import *
from datetime import datetime

# Load your JSON data
with open(r'C:\Users\Pinak\OneDrive\Desktop\SKU (1).json', 'r') as f:  # Use a raw string
    data = json.load(f)# Access the relevant key if it's still part of the data structure

# Iterate over the data and add it to the database
for item in data:
    date_assigned = datetime.strptime(item["date_assigned"], "%d-%m-%Y").date()
    
    # Create ProductionShiftAssignments object
    production_shift_assignment = ProductionShiftAssignments(
        assignment_id=item["assignment_id"],
        shift_id=item["shift_id"],  # Reference to WorkShift
        employee_id=item["employee_id"],  # Reference to Employee
        date_assigned=date_assigned
    )
    
    # Save to the database
    production_shift_assignment.save()

print("Data successfully added to the database.")
