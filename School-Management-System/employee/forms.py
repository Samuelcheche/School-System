from django import forms
from .models import OfficialInfo, PersonalInfo

class OfficialInfoForm(forms.ModelForm):
    class Meta:
        model = OfficialInfo
        fields = ("official_register_number", "official_register_date")
        widgets = {
            'official_register_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'LM10'}),
            'official_register_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
        }


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ("full_name", "dob", "another_fullname", "national_id", "employee_avatar")
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'another_fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'national_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'employee_avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }