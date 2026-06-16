from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Employee
from django.utils import timezone
from .models import Employee, Attendance
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta

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

def attendance_report(request):

    report = []

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    employee_id = request.GET.get("employee")
    today = timezone.now().date()
    monday = today - timedelta(days=today.weekday())
    saturday = monday + timedelta(days=5)
    employees = Employee.objects.filter(
        is_active=True,
        employee_type='daily'
    )
    if from_date and to_date:

        employees = Employee.objects.filter(is_active=True)

        for emp in employees:

            days = Attendance.objects.filter(
                employee=emp,
                date__range=[from_date, to_date]
            ).count()

            amount = days * emp.daily_wage

            report.append({
                "name": emp.name,
                "days": days,
                "wage": emp.daily_wage,
                "amount": amount
            })

    return render(
        request,
        "attendance_report.html",
        {
            "report": report,
             "employees": employees
        }
    )