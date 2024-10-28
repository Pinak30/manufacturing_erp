from mongoengine import *
from django import forms
from .models import *
from django.core.validators import RegexValidator


class LoginForm(forms.Form):
    email_id = forms.CharField(
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
        ('inventory', 'Inventory'),
        ('production', 'Production'),
        ('finance', 'Finance'),
    ]
    
    contact_number_validator = RegexValidator(r'^\d{10,15}$', 'Contact number must be between 10 to 15 digits.')
    employee_name = forms.CharField(max_length=100)
    designation = forms.ChoiceField(choices=DESIGNATION_CHOICES)
    date_of_joining = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    shift_timings = forms.CharField()
    email_id = forms.EmailField()
    contact_info = forms.CharField(validators=[contact_number_validator], max_length=15)
    emergency_contact = forms.CharField(validators=[contact_number_validator], max_length=15)
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=20)
    work_history = forms.CharField(widget=forms.Textarea, required=False)

    def generate_employee_id(self):
        prefix = "EMP"
        try:
            last_employee = Employee.objects.order_by('-employee_id').first()
            if last_employee:
                last_id = int(last_employee.employee_id.replace(prefix, ""))
                new_id = f"{prefix}{last_id + 1:05d}"
            else:
                new_id = f"{prefix}00001"
        except DoesNotExist:
            new_id = f"{prefix}00001"
        return new_id

    def save(self, commit=True):
        designation_instance = Designation.objects.get(designation_id=self.cleaned_data['designation'])

        # Automatically generate employee_id
        employee_id = self.generate_employee_id()

        employee = Employee(
            employee_id=employee_id,
            employee_name=self.cleaned_data['employee_name'],
            designation_id=designation_instance,
            date_of_joining=self.cleaned_data['date_of_joining'],
            shift_timings=self.cleaned_data['shift_timings'],
            email_id=self.cleaned_data['email_id'],
            contact_info=self.cleaned_data['contact_info'],
            emergency_contact=self.cleaned_data['emergency_contact'],
            role=self.cleaned_data['role'],
            password=self.cleaned_data['password'],
            work_history=self.cleaned_data['work_history']
        )
        
        if commit:
            employee.save()
        return employee