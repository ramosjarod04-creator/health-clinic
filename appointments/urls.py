from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_main, name='appointment_main'),
    path('patients/', views.patients_list, name='patients_list'), # For Sidebar 'Patients'
    path('all-appointments/', views.all_appointments, name='all_appointments'), # For Sidebar 'Appointments'
    path('delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),
    path('status/<int:pk>/<str:status>/', views.update_status, name='update_status'),
    path('appointment/cancel/<int:pk>/', views.cancel_appointment, name='cancel_appointment'),
]