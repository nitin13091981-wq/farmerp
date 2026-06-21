from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('attendance/', views.attendance_entry, name='attendance'),
    path('labour/add/', views.add_labour, name='add_labour'),
    path('attendance-report/', views.attendance_report, name='attendance_report'),

    path(
        'attendance/edit/<int:id>/',
        views.edit_attendance,
        name='edit_attendance'
    ),

    path(
        'attendance/delete/<int:id>/',
        views.delete_attendance,
        name='delete_attendance'
    ),
]