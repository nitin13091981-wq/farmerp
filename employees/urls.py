from django.urls import path
from .views import dashboard, attendance_entry

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('attendance/', attendance_entry, name='attendance'),
]