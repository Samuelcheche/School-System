from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import *
from .forms import OfficialInfoForm, PersonalInfoForm

# Create your views here.
def employee_list(request):
    official_info = OfficialInfo.objects.order_by('id')
    personal_info = PersonalInfo.objects.order_by('id')
    employee_rows = zip(official_info, personal_info)
    context = {
        "employee_rows": employee_rows
    }
    return render(request, "employee/employee_list.html", context)


def create_employee(request):
    official_form = OfficialInfoForm()
    personal_form = PersonalInfoForm()

    if request.method == "POST":
        official_form = OfficialInfoForm(request.POST)
        personal_form = PersonalInfoForm(request.POST, request.FILES or None)

        if official_form.is_valid() and personal_form.is_valid():
            with transaction.atomic():
                official_form.save()
                personal_form.save()
            messages.success(request, "Employee Registration Successfully!")
            return redirect("create_employee")

        messages.error(request, "Please correct the errors and submit again.")

    context = {
        "official_form": official_form,
        "personal_form": personal_form,
    }
    return render(request, "employee/registration.html", context)


