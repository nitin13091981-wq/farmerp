from django.urls import path
from .views import home, attendance_entry, add_labour

urlpatterns = [
    path('', home, name='home'),
    path('attendance/', attendance_entry, name='attendance'),
    path('labour/add/', add_labour, name='add_labour'),
]