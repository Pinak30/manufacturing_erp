from django.db import models

# Create your models here.

class Employee(models.Model):
    _id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=20, default='12345678')
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=30)
    contact_no = models.BigIntegerField(null=False, default=9999999999)
    emrg_contact_no = models.BigIntegerField(null=True)
    date_of_joining = models.DateField()
    history = models.TextField(max_length=500,null=True)

class WorkDetails(models.Model):
    shift_time = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    eid = models.ForeignKey(Employee, on_delete=models.CASCADE)