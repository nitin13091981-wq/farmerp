from django.shortcuts import render, redirect
from .models import Employee
from django.utils import timezone
from .models import Employee, Attendance


def dashboard(request):
    return render(request, 'dashboard.html')

def attendance_entry(request):

    if request.method == "POST":

        employee_ids = request.POST.getlist('employees')

        today = timezone.now().date()

        for emp_id in employee_ids:

            employee = Employee.objects.get(id=emp_id)

            Attendance.objects.get_or_create(
                employee=employee,
                date=today,
                defaults={
                    'status': 'full'
                }
            )

        return redirect('attendance')

    employees = Employee.objects.filter(is_active=True)

    return render(
        request,
        'attendance.html',
        {
            'employees': employees
        }
    )