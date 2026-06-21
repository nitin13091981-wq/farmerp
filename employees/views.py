from urllib import request

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Employee
from django.utils import timezone
from .models import Employee, Attendance
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from datetime import datetime 

#@login_required
def home(request):
    return render(request, 'home.html')

#@login_required
def add_labour(request):

    if request.method == "POST":

        name = request.POST.get("name")
        wage = request.POST.get("wage")
        phone = request.POST.get("phone")
       
        if name and wage:
            Employee.objects.create(
                name=name,
                phone=phone if phone else "",
                employee_type="daily",
                daily_wage=wage,
                joining_date=timezone.now().date()
            )
        messages.success(
         request,
            f"{name} ko Farm Sahayogi ke roop mein safalta se joda gaya."
        )
        return redirect('home')

    return render(request, 'add_labour.html')

def dashboard(request):
    return render(request, 'dashboard.html')




def attendance_entry(request):
    if request.method == "POST":

        attendance_date = request.POST.get("attendance_date")

        if attendance_date:
            today = attendance_date
        else:
            today = timezone.now().date()

        employee_ids = request.POST.getlist("employees")

        # Existing Employees
        for emp_id in employee_ids:

            employee = Employee.objects.get(id=emp_id)

            wage = request.POST.get(
                f"wage_{emp_id}",
                employee.daily_wage
            )

            attendance, created = Attendance.objects.get_or_create(
                employee=employee,
                date=today,
                defaults={
                    "status": "full",
                    "actual_wage": wage
                }
            )

            if not created:
                attendance.actual_wage = wage
                attendance.status = "full"
                attendance.save()

        # New Employee
        new_name = request.POST.get("new_name")
        new_wage = request.POST.get("new_wage")

        if new_name and new_wage:

            employee = Employee.objects.create(
                name=new_name,
                phone="TEMP",
                employee_type="daily",
                daily_wage=new_wage,
                joining_date=today
            )

            Attendance.objects.create(
                employee=employee,
                date=today,
                status="full",
                actual_wage=new_wage
            )

        messages.success(
            request,
            "उपस्थिति एवं पारिश्रमिक सफलतापूर्वक सुरक्षित कर दिया गया।"
        )

        return redirect("attendance")

    employees = Employee.objects.filter(
        is_active=True
    ).exclude(
        employee_type="permanent"
    )

    return render(
        request,
        "attendance.html",
        {
            "employees": employees
        }
    )





#@login_required
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        # Temporary Login
        if username == "admin" and password == "admin123":

            request.session['logged_in'] = True

            return redirect('home')

        messages.error(
            request,
            "Galat Username ya Password"
        )

    return render(request, "login.html")


from django.db.models import Count

from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

def attendance_report(request):

    report = []

    today = timezone.now().date()

    weekday = today.weekday()

    if weekday == 0:
        start_date = today - timedelta(days=6)
    else:
        start_date = today - timedelta(days=(weekday - 1))

    end_date = start_date + timedelta(days=5)

    from_date = request.GET.get(
        "from_date",
        start_date.strftime("%Y-%m-%d")
    )

    to_date = request.GET.get(
        "to_date",
        end_date.strftime("%Y-%m-%d")
    )

    employee_id = request.GET.get("employee")

    employees = Employee.objects.filter(
        is_active=True
    )

    if employee_id:
        employees = employees.filter(id=employee_id)

    from_dt = datetime.strptime(
        from_date,
        "%Y-%m-%d"
    ).date()

    to_dt = datetime.strptime(
        to_date,
        "%Y-%m-%d"
    ).date()

    week_dates = []

    current = from_dt

    while current <= to_dt:
        week_dates.append(current)
        current += timedelta(days=1)

    total_amount = 0

    for emp in employees:

        attendance_map = {}

        amount = 0

        days = 0

        for day in week_dates:

            attendance = Attendance.objects.filter(
                employee=emp,
                date=day
            ).first()

            attendance_map[day] = attendance

            if attendance:

                days += 1

                amount += float(
                    attendance.actual_wage or 0
                )

        total_amount += amount


        report.append({
            "id": emp.id,
            "name": emp.name,
            "days": days,
            "amount": amount,
            "attendance_map": attendance_map,
        })

        

    return render(
        request,
        "attendance_report.html",
        {
            "report": report,
            "employees": Employee.objects.filter(
                is_active=True
            ),
            "week_dates": week_dates,
            "from_date": from_date,
            "to_date": to_date,
            "total_amount": total_amount,
        }
    )


def edit_attendance(request, id):

    attendance = Attendance.objects.get(id=id)

    if request.method == "POST":

        attendance.actual_wage = request.POST.get(
            "actual_wage"
        )

        attendance.save()

        messages.success(
            request,
            f"{attendance.employee.name} का पारिश्रमिक सफलतापूर्वक संशोधित किया गया।"
        )
        return redirect("attendance_report")

    return render(
        request,
        "edit_attendance.html",
        {
            "attendance": attendance
        }
    )


def delete_attendance(request, id):
    attendance = Attendance.objects.get(id=id)
    attendance.delete()
    messages.success(
        request,
        f"{attendance.employee.name} की उपस्थिति रिकॉर्ड हटायी गयी।"
    )
    return redirect("attendance_report")

