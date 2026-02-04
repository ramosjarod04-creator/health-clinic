from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash
from django.db.models import Sum, Q
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Appointment

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('appointment_main')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_settings(request):
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.email = request.POST.get('email')
            request.user.save()
            messages.success(request, 'Profile information updated.')
        elif 'change_password' in request.POST:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
            else:
                messages.error(request, 'Please correct the errors in the password form.')
        return redirect('profile_settings')
    
    password_form = PasswordChangeForm(request.user)
    return render(request, 'appointments/profile.html', {'password_form': password_form})

@login_required
def appointment_main(request):
    if request.method == "POST":
        pricing_map = {'checkup': 500.0, 'consultation': 800.0, 'surgery': 1500.0, 'therapy': 1200.0}
        selected_service = request.POST.get('service_type')
        assigned_fee = pricing_map.get(selected_service, 500.00)

        Appointment.objects.create(
            patient_name=request.POST.get('patient_name'),
            doctor_name=request.POST.get('doctor_name'),
            service_type=selected_service,
            fee=assigned_fee,
            date=request.POST.get('date'),
            time=request.POST.get('time'),
            created_by=request.user
        )
        return redirect('appointment_main')

    all_appointments = Appointment.objects.all()
    stats = {
        'total_patients': User.objects.filter(is_staff=False).count(),
        'earnings': all_appointments.filter(status='completed').aggregate(Sum('fee'))['fee__sum'] or 0,
        'admitted': all_appointments.filter(status='admitted').count(),
        'discharged': all_appointments.filter(status='discharged').count(),
        'pending': all_appointments.filter(status='pending').count(),
    }

    context = {
        'stats': stats,
        'available_doctors': User.objects.filter(Q(is_superuser=True) | Q(is_staff=True)),
        'service_choices': Appointment.SERVICE_CHOICES,
    }

    if request.user.is_staff:
        context['appointments'] = all_appointments.order_by('-date')
        return render(request, 'appointments/admin_dashboard.html', context)
    else:
        context['appointments'] = all_appointments.filter(created_by=request.user).order_by('-date')
        return render(request, 'appointments/patient_booking.html', context)

@login_required
def update_status(request, pk, status):
    if request.user.is_staff:
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.status = status
        appointment.save()
        return redirect('all_appointments')
    return redirect('appointment_main')

@login_required
def delete_appointment(request, pk):
    if request.user.is_staff:
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.delete()
        return redirect('all_appointments')
    return redirect('appointment_main')

@login_required
def patients_list(request):
    if not request.user.is_staff: return redirect('appointment_main')
    patients = User.objects.filter(is_staff=False)
    return render(request, 'appointments/patients_list.html', {'patients': patients})

@login_required
def all_appointments(request):
    if not request.user.is_staff: return redirect('appointment_main')
    appointments = Appointment.objects.all().order_by('-date')
    return render(request, 'appointments/all_appointments.html', {'appointments': appointments})

@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, created_by=request.user)
    if appointment.status == 'pending':
        appointment.delete()
    return redirect('appointment_main')