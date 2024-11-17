from mongoengine import Document, StringField, ReferenceField, IntField, DateField, DecimalField

class Material(Document):
    material_id = IntField(primary_key=True)  
    material_name = StringField(required=True)
    material_state = StringField()
    description = StringField()
    life_span = IntField()  
    life_span_measure = StringField()


class Sku(Document):
    sku_id = IntField(primary_key=True)  
    sku_name = StringField(required=True)
    material_type = StringField()
    package_type = StringField()
    net_qty = IntField()
    unit_of_measurement = StringField()
    unit_price = DecimalField(precision=2)
    active = IntField() 


class RawMaterial(Document):
    raw_material_id = IntField(primary_key=True, max_length=100)  # Primary Key
    raw_material_name = StringField(required=True)
    raw_material_type = StringField()
    raw_material_description = StringField()
    raw_material_unit_price = DecimalField(precision=2)
    raw_material_measurement_unit = StringField()
    raw_material_life_span = IntField()
    raw_material_life_span_measure = StringField()


class InventoryRawMaterial(Document):
    inventory_id = IntField(primary_key=True, max_length=100)  # Primary Key
    raw_material_id = ReferenceField(RawMaterial, reverse_delete_rule=4)  # Foreign Key
    quantity_in_stock = IntField(required=True)
    location = StringField()
    manufacturing_date = DateField()
    order_date = DateField()


class PurchaseOrder(Document):
    purchase_order_id = IntField(primary_key=True, max_length=100)  # Primary Key
    supplier_id = IntField() 
    order_date = DateField()


class PurchaseOrderItem(Document):
    purchase_order_item_id = IntField(primary_key=True, max_length=100)  # Primary Key
    purchase_order_id = ReferenceField(PurchaseOrder, reverse_delete_rule=4)  # Foreign Key
    raw_material_id = ReferenceField(RawMaterial, reverse_delete_rule=4)  # Foreign Key
    quantity = IntField(required=True)
    price_per_unit = DecimalField(precision=2)


class ProductionBatch(Document):
    batch_id = IntField(primary_key=True, max_length=100)  # Primary Key
    batch_date = DateField(required=True)
    sku_id = ReferenceField(Sku, reverse_delete_rule=4)  # Foreign Key
    quantity_produced = IntField(required=True)


class BatchIngredient(Document):
    batch_ingredient_id = IntField(primary_key=True, max_length=100)  # Primary Key
    batch_id = ReferenceField(ProductionBatch, reverse_delete_rule=4)  # Foreign Key
    raw_material_id = ReferenceField(RawMaterial, reverse_delete_rule=4)  # Foreign Key
    quantity_used = IntField(required=True)


class ProductInventory(Document):
    product_inventory_id = IntField(primary_key=True, max_length=100)  # Primary Key
    sku_id = ReferenceField(Sku, reverse_delete_rule=4)  # Foreign Key
    quantity = IntField(required=True)
    location = StringField()
    manufacturing_date = DateField()
    expiry_date = DateField()
