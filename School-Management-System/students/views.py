from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.utils import timezone
from .forms import CreateStudent, CreateStudentRegistration

# Create your views here.
def student_list(request):
    students = StudentInfo.objects.all()
    paginator = Paginator(students, 1)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)

    context = {
        "students": paged_students
    }
    return render(request, "students/student_list.html", context)


def single_student(request, student_id):
    single_student = get_object_or_404(StudentInfo, pk=student_id)
    context = {
        "single_student": single_student
    }
    return render(request, "students/student_details.html", context)


def student_regi(request):
    if request.method == "POST":
        forms = CreateStudentRegistration(request.POST)

        if forms.is_valid():
            forms.save()
        messages.success(request, "Student Registration Successfully!")
        return redirect("student_list")
    else:
        forms = CreateStudentRegistration()

    context = {
        "forms": forms
    }
    return render(request, "students/registration.html", context)


def edit_student(request, pk):
    student_edit = StudentInfo.objects.get(id=pk)
    edit_forms = CreateStudent(instance=student_edit)

    if request.method == "POST":
        edit_forms = CreateStudent(request.POST, instance=student_edit)

        if edit_forms.is_valid():
            edit_forms.save()
            messages.success(request, "Edit Student Info Successfully!")
            return redirect("student_list")

    context = {
        "edit_forms": edit_forms
    }
    return render(request, "students/edit_student.html", context)


def delete_student(request, student_id):
    student_delete = StudentInfo.objects.get(id=student_id)
    student_delete.delete()
    messages.success(request, "Delete Student Info Successfully")
    return redirect("student_list")


def attendance_count(request):
    class_name = ""
    student_list = []
    today = timezone.localdate()

    if request.method == "POST":
        class_name = request.POST.get("class_name", "").strip()
        present_student_ids = set(request.POST.getlist("present_students"))

        if not class_name:
            messages.error(request, "Please provide a class name.")
        else:
            student_qs = StudentInfo.objects.filter(class_type__class_short_form__iexact=class_name)
            if not student_qs.exists():
                messages.error(request, "No students found for this class.")
            else:
                for student in student_qs:
                    status_value = 1 if str(student.id) in present_student_ids else 0
                    Attendance.objects.update_or_create(
                        student=student,
                        date=today,
                        defaults={"status": status_value}
                    )
                messages.success(request, "Attendance saved successfully.")
                student_list = list(student_qs)

    elif request.method == "GET":
        class_name = request.GET.get("class_name", "").strip()
        if class_name:
            student_list = list(StudentInfo.objects.filter(class_type__class_short_form__iexact=class_name))

    if student_list:
        attendance_map = {
            item.student_id: item.status
            for item in Attendance.objects.filter(student__in=student_list, date=today)
        }
        for student in student_list:
            student.is_present_today = attendance_map.get(student.id, 0) == 1

    context = {
        "student_list": student_list,
        "class_name": class_name,
    }
    return render(request, "students/attendance_count.html", context)

