from django import forms
from .models import StudentInfo, StudentClassInfo, StudentSectionInfo, StudentShiftInfo

class CreateStudent(forms.ModelForm):
    class Meta:
        model = StudentInfo
        exclude = ("student_img", "fathers_img", "mothers_img", )

        widgets = {
            'academic_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2018-2020'}),
            'admission_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2018-12-31'}),
            'admission_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: LM01'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: John Doe'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 30'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'class_type': forms.Select(attrs={'class': 'form-control'}),
            'section_type': forms.Select(attrs={'class': 'form-control'}),
            'shift_type': forms.Select(attrs={'class': 'form-control'}),
            'fathers_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Steve Smith'}),
            'fathers_nid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 3732106814'}),
            'fathers_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 01884334899'}),
            'mothers_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Steve Smith'}),
            'mothers_nid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 3732106814'}),
            'mothers_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 01884334899'}),
        }


class CreateStudentRegistration(forms.ModelForm):
    class_type = forms.ChoiceField(
        choices=(
            ("FORM1", "Form 1"),
            ("FORM2", "Form 2"),
            ("FORM3", "Form 3"),
            ("FORM4", "Form 4"),
        ),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = StudentInfo
        exclude = (
            "student_img", "fathers_img", "mothers_img",
            "class_type", "section_type", "shift_type",
        )

        widgets = {
            'academic_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2018-2020'}),
            'admission_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2018-12-31'}),
            'admission_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: LM01'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: John Doe'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 30'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'fathers_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Steve Smith'}),
            'fathers_nid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 3732106814'}),
            'fathers_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 01884334899'}),
            'mothers_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Steve Smith'}),
            'mothers_nid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 3732106814'}),
            'mothers_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 01884334899'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        selected_class_short = self.cleaned_data["class_type"]
        class_name = selected_class_short.replace("FORM", "Form ")
        class_obj, _ = StudentClassInfo.objects.get_or_create(
            class_short_form=selected_class_short,
            defaults={"class_name": class_name}
        )

        default_section, _ = StudentSectionInfo.objects.get_or_create(section_name="General")
        default_shift, _ = StudentShiftInfo.objects.get_or_create(shift_name="Morning")

        instance.class_type = class_obj
        instance.section_type = default_section
        instance.shift_type = default_shift

        if commit:
            instance.save()
        return instance

