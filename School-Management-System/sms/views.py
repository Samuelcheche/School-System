from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from students.models import StudentInfo, Attendance
from teachers.models import TeacherInfo
from employee.models import EmployeeInfo

@login_required
def index(request):
    today = timezone.localdate()
    display_name = request.user.first_name.strip() if request.user.first_name else request.user.username
    context = {
        "display_name": display_name,
        "student_count": StudentInfo.objects.count(),
        "teacher_count": TeacherInfo.objects.count(),
        "employee_count": EmployeeInfo.objects.count(),
        "attendance_count": Attendance.objects.filter(date=today).count(),
    }
    return render(request, "home.html", context)



