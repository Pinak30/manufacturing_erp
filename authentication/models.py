from django.db import models

# Create your models here.

class Employee(models.Model):
    _id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=30)
    date_of_joining = models.DateField()

