from mongoengine import Document, StringField, EmailField, DateField, IntField, DecimalField, ReferenceField, ListField


class Department(Document):
    department_id = StringField(primary_key=True, max_length=100)
    department_name = StringField(required=True, max_length=255)


class Designation(Document):
    designation_id = StringField(primary_key=True, max_length=100)
    designation_name = StringField(required=True, max_length=255)
    department_id = ReferenceField(Department, reverse_delete_rule=4)  # Foreign Key to Department


class Employee(Document):
    employee_id = StringField(primary_key=True, max_length=100)
    employee_name = StringField(required=True, max_length=255)
    designation_id = ReferenceField(Designation, reverse_delete_rule=4)  # Foreign Key to Designation
    date_of_joining = DateField(required=True)
    shift_timings = StringField(max_length=100)  
    email_id = EmailField()
    contact_info = StringField(max_length=15) 
    emergency_contact = StringField(max_length=15)
    role = StringField()
    password = StringField(max_length=20)
    work_history = StringField() 


class Payroll(Document):
    payroll_id = IntField(primary_key=True, max_length=100)
    salary = DecimalField(required=True, precision=2) 
    bonus = DecimalField(precision=2) 


class SalaryAttendance(Document):
    salary_attendance_id = StringField(primary_key=True, max_length=100)
    employee_id = ReferenceField(Employee, reverse_delete_rule=4)  # FK to Employee
    payroll_id = ReferenceField(Payroll, reverse_delete_rule=4)    # FK to Payroll
    attendance_date = DateField(required=True)
    leave_balance = IntField(default=0)  # Optional, can default to 0
    net_salary = DecimalField(precision=2, required=False) 