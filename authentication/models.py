from mongoengine import Document, StringField, EmailField, DateField, IntField, DecimalField, ReferenceField, ListField

class Employee(Document):
    name = StringField(required=True, max_length=255)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, max_length=255)
    department = StringField(required=True, max_length=100)
    role = StringField(required=True, max_length=100)
    contact_no = StringField(max_length=15)  # adjust as needed
    emrg_contact_no = StringField(max_length=15)
    date_of_joining = DateField(required=True)
    history = StringField()

class WorkDetails(Document):
    employee = ReferenceField(Employee, reverse_delete_rule=4)  # 4 corresponds to CASCADE
    shift_time = StringField()  # MongoEngine doesn't have TimeField; consider using StringField for time
    salary = DecimalField(precision=2)
