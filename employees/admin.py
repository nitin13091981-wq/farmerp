from django.contrib import admin

from .models import (
    Employee,
    Attendance,
    Expenditure,
    AdvancePayment,
    SalarySlip,
)

admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Expenditure)
admin.site.register(AdvancePayment)
admin.site.register(SalarySlip)