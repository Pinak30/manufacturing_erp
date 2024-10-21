from mongoengine import *
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))

class SignUpForm(forms.Form):
    DESIGNATION_CHOICES = [(des.designation_id, des.designation_name) for des in Designation.objects.all()]
    ROLE_CHOICES = [
        ('HR', 'HR'),
        ('Inventory', 'Inventory'),
        ('Production', 'Production'),
        ('Finance', 'Finance'),
    ]

    contact_number_validator = RegexValidator(r'^\d{10,15}$', 'Contact number must be between 10 to 15 digits.')
    employee_id = forms.CharField(max_length=100)
    payroll_id = forms.CharField(max_length=100)
    salary_attendance_id = forms.CharField(max_length=100)
    contact_no = forms.CharField(validators=[contact_number_validator], max_length=15)
    emrg_contact_no = forms.CharField(validators=[contact_number_validator], max_length=15)
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), max_length=255)
    designation = forms.ChoiceField(choices=DESIGNATION_CHOICES)
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    date_of_joining = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    history = forms.CharField(required=False, widget=forms.Textarea)
    shift_time = forms.CharField()
    salary = forms.DecimalField(max_digits=10, decimal_places=2)

    def save(self, commit=True):
        designation = Designation.objects.get(designation_id=self.cleaned_data['designation'])

        employee = Employee(
            employee_id=self.cleaned_data['employee_id'],
            email_id=self.cleaned_data['email'],
            employee_name=self.cleaned_data['name'],
            designation_id=designation,  # Reference the selected designation object
            contact_info=self.cleaned_data['contact_no'],
            emergency_contact=self.cleaned_data['emrg_contact_no'],
            role=self.cleaned_data['role'],
            date_of_joining=self.cleaned_data['date_of_joining'],
            work_history=self.cleaned_data['history'],
            shift_timings=self.cleaned_data['shift_time'],
            password=self.cleaned_data['password']
        )
        employee.save()

        payroll = Payroll(
            payroll_id=self.cleaned_data['payroll_id'],
            salary=self.cleaned_data['salary'],
            bonus=0.00
        )
        payroll.save()

        salary_attendance = SalaryAttendance(
            salary_attendance_id=self.cleaned_data['salary_attendance_id'],
            employee_id=employee,
            payroll_id=payroll,
            attendance_date=self.cleaned_data['date_of_joining'],
            net_salary=self.cleaned_data['salary'],
        )
        salary_attendance.save()

        return employee