from mongoengine import Document, StringField, ReferenceField, IntField, DateField, ListField
from inventory.models import Sku, RawMaterial
from authentication.models import  Employee

class BOM(Document):
    bom_id = StringField(primary_key=True, max_length=100)  # Primary Key
    sku_id = ReferenceField(Sku, reverse_delete_rule=4) # Foreign Key from Inventory app
    raw_material_id = ReferenceField(RawMaterial, reverse_delete_rule=4) # Foreign Key from Inventory app
    qty_required = IntField(required=True)  
    machine_required = StringField()  
    designation_required = StringField() 
    by_product = StringField() 
    qty_to_be_produced = IntField(required=True)  


class ProductionOrder(Document):
    production_order_id = StringField(primary_key=True, max_length=100)  # Primary Key
    sku_id = ReferenceField(Sku, reverse_delete_rule=4) # Foreign Key from Inventory app 
    order_date = DateField(required=True) 
    planned_quantity = IntField(required=True)  
    status = StringField()  


class PlanProduction(Document):
    plan_id = StringField(primary_key=True, max_length=100)  # Primary Key
    production_order_id = ReferenceField(ProductionOrder, reverse_delete_rule=4)  # Foreign Key
    bom_id = ReferenceField(BOM, reverse_delete_rule=4)  # Foreign Key
    batch = StringField() 
    no_of_batches = IntField(required=True) 
    plan_date = DateField(required=True) 
    reorder_status = StringField()  
    status = StringField() 


class ProductionBatch(Document):
    batch_id = StringField(primary_key=True, max_length=100)  # Primary Key
    production_order_id = ReferenceField(ProductionOrder, reverse_delete_rule=4)  # Foreign Key
    batch_date = DateField(required=True) 
    quantity_produced = IntField(required=True)  


class WorkShift(Document):
    shift_id = StringField(primary_key=True, max_length=100)  # Primary Key
    shift_type = StringField(required=True)  
    shift_start_time = StringField(required=True) 
    shift_end_time = StringField(required=True)  


class ProductionShiftAssignments(Document):
    assignment_id = StringField(primary_key=True, max_length=100)  # Primary Key
    shift_id = ReferenceField(WorkShift, reverse_delete_rule=4)  # Foreign Key
    employee_id = ReferenceField(Employee, reverse_delete_rule=4)  # Foreign Key
    date_assigned = DateField(required=True)  



