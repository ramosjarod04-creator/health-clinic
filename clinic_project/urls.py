from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings  # Required for static handling
from django.conf.urls.static import static  # Required for static handling
from appointments import views 
from django.views.generic.base import RedirectView

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls), 

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # Core Navigation
    path('', views.appointment_main, name='appointment_main'),
    path('profile/', views.profile_settings, name='profile_settings'),
    path('patients/', views.patients_list, name='patients_list'),

    # Appointment Management
    path('appointments/all/', views.all_appointments, name='all_appointments'),
    path('status/<int:pk>/<str:status>/', views.update_status, name='update_status'),
    path('delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),
    path('cancel/<int:pk>/', views.cancel_appointment, name='cancel_appointment'),

    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
]

# Serving static files in development (WhiteNoise handles production)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)