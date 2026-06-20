from django import views
from django.urls import path
from .views import home, attendance_entry, add_labour, login_view,attendance_report,edit_attendance,delete_attendance
urlpatterns = [
    path('', login_view, name='login'),
    path('home/', home, name='home'),
    path('attendance/', attendance_entry, name='attendance'),
    path('labour/add/', add_labour, name='add_labour'),
    path('attendance-report/', attendance_report, name='attendance_report'),
    path("attendance/edit/[int:id](int:id)/",views.edit_attendance,name="edit_attendance"),
    path("attendance/delete/[int:id](int:id)/",views.delete_attendance,name="delete_attendance"),

]