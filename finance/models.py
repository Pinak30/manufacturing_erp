from mongoengine import Document, StringField, DateField, FloatField, ReferenceField, IntField, ListField
from inventory.models import RawMaterial


class GeneralLedger(Document):
    ledger_id = StringField(primary_key=True, max_length=100)
    ledger_name = StringField(required=True, max_length=255)
    opening_balance = FloatField(required=True)
    closing_balance = FloatField(required=True)


class Account(Document):
    account_id = IntField(primary_key=True, max_length=100)
    account_name = StringField(required=True, max_length=255)
    account_type = StringField(required=True)
    balance = FloatField(required=True)


class Customer(Document):
    customer_id = IntField(primary_key=True, max_length=100)
    customer_name = StringField(required=True, max_length=255)
    customer_email = StringField(required=True, max_length=100)
    customer_phone = StringField(required=True, max_length=15)


class Invoice(Document):
    invoice_id = StringField(primary_key=True, max_length=100)
    invoice_date = DateField(required=True)
    customer_id = ReferenceField(Customer, reverse_delete_rule=4)  # Foreign key to Customer
    amount = FloatField(required=True)


class Payment(Document):
    payment_id = StringField(primary_key=True, max_length=100)
    payment_date = DateField(required=True)
    amount_paid = FloatField(required=True)
    invoice_id = ReferenceField(Invoice, reverse_delete_rule=4)  # Foreign key to Invoice


class Supplier(Document):
    supplier_id = IntField(primary_key=True, max_length=100)
    supplier_name = StringField(required=True, max_length=255)
    supplier_contact = StringField(required=True, max_length=15)
    raw_material_id = ListField(ReferenceField(RawMaterial, reverse_delete_rule=4))
    description = StringField(max_length=255)


class PurchaseOrderFinance(Document):
    purchase_order_id = IntField(primary_key=True, max_length=100)
    order_date = DateField(required=True)
    supplier_id = ReferenceField(Supplier, reverse_delete_rule=4)  # Foreign key to Supplier
    total_amount = FloatField(required=True)
    expected_delivery_date = DateField()


class Expense(Document):
    expense_id = StringField(primary_key=True, max_length=100)
    expense_type = StringField(required=True, max_length=100)
    amount = FloatField(required=True)
    purchase_order_id = ReferenceField(PurchaseOrderFinance, reverse_delete_rule=4)  # Foreign key to Purchase Order


class Transaction(Document):
    transaction_id = StringField(primary_key=True, max_length=100)
    transaction_date = DateField(required=True)
    amount = FloatField(required=True)
    account_id = ReferenceField(Account, reverse_delete_rule=4)  # Foreign key to Account
    ledger_id = ReferenceField(GeneralLedger, reverse_delete_rule=4)  # Foreign key to General Ledger
    payment_id = ReferenceField(Payment, reverse_delete_rule=4)  # Foreign key to Payment
    expense_id = ReferenceField(Expense, reverse_delete_rule=4)  # Foreign key to Exxpense


class Budget(Document):
    budget_id = StringField(primary_key=True, max_length=100)
    year = IntField(required=True)
    total_budget = FloatField(required=True)
    allocated_amount = FloatField(required=True)


