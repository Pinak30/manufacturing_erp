from mongoengine import *
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
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
    # Define department choices
    DEPARTMENT_CHOICES = [
        ('Inventory', 'Inventory'),
        ('Production', 'Production'),
        ('Finance', 'Finance'),
        ('HR', 'HR'),
    ]

    # Validator for contact numbers (only digits)
    contact_number_validator = RegexValidator(r'^\d{10,15}$', 'Contact number must be between 10 to 15 digits.')

    # Use CharField with a validator for contact numbers
    contact_no = forms.CharField(validators=[contact_number_validator], max_length=15)
    emrg_contact_no = forms.CharField(validators=[contact_number_validator], max_length=15)

    # Fields from WorkDetails model
    shift_time = forms.CharField(widget=forms.TimeInput(attrs={'type': 'time'}))  # Use CharField for time
    salary = forms.DecimalField(max_digits=10, decimal_places=2)

    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), max_length=255)
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
    role = forms.CharField(max_length=100)
    date_of_joining = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    history = forms.CharField(required=False, widget=forms.Textarea)

    def save(self, commit=True):
        employee = Employee(
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            department=self.cleaned_data['department'],
            role=self.cleaned_data['role'],
            contact_no=self.cleaned_data['contact_no'],
            emrg_contact_no=self.cleaned_data['emrg_contact_no'],
            date_of_joining=self.cleaned_data['date_of_joining'],
            history=self.cleaned_data['history'],
        )
        employee.save()

        work_details = WorkDetails(
            employee=employee,
            shift_time=self.cleaned_data['shift_time'],
            salary=self.cleaned_data['salary'],
        )
        work_details.save()

        return employee