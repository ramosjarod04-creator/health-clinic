from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from appointments import views  

urlpatterns = [
    path('admin/', admin.site.urls), 

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('', views.appointment_main, name='appointment_main'),
    path('profile/', views.profile_settings, name='profile_settings'),
    path('patients/', views.patients_list, name='patients_list'),
    path('appointments/all/', views.all_appointments, name='all_appointments'),
    path('status/<int:pk>/<str:status>/', views.update_status, name='update_status'),
    path('delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),
    path('cancel/<int:pk>/', views.cancel_appointment, name='cancel_appointment'),
]