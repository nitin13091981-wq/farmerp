from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Employee
from django.utils import timezone
from .models import Employee, Attendance
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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

            return redirect('add_labour')

    return render(request, 'add_labour.html')

def dashboard(request):
    return render(request, 'dashboard.html')



#@login_required
def attendance_entry(request):

    if request.method == "POST":

        attendance_date = request.POST.get('attendance_date')
        if attendance_date:
            today = attendance_date
        else:
            today = timezone.now().date()
        # Existing employees attendance
        employee_ids = request.POST.getlist('employees')

        for emp_id in employee_ids:

            employee = Employee.objects.get(id=emp_id)

            Attendance.objects.get_or_create(
                employee=employee,
                date=today,
                defaults={
                    'status': 'full'
                }
            )

        # New labour entry
        new_name = request.POST.get('new_name')
        new_wage = request.POST.get('new_wage')

        print("NAME =", new_name)
        print("WAGE =", new_wage)

        if new_name and new_wage:

            employee = Employee.objects.create(
                name=new_name,
                phone=f"TEMP-{today}-{new_name}",
                employee_type='daily',
                daily_wage=new_wage,
                joining_date=today
            )

            Attendance.objects.create(
                employee=employee,
                date=today,
                status='full'
            )
        messages.success(request, "हाज़िरी सफलतापूर्वक सुरक्षित हो गई।")
        return redirect('attendance')

    employees = Employee.objects.filter(is_active=True)

    return render(
        request,
        'attendance.html',
        {
            'employees': employees
        }
    )
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