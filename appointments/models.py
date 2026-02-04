from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
        ('completed', 'Completed'),
        ('denied', 'Denied'),
    ]

    SERVICE_CHOICES = [
        ('checkup', 'General Checkup (₱500)'),
        ('consultation', 'Specialist Consultation (₱800)'),
        ('surgery', 'Minor Surgery (₱1,500)'),
        ('therapy', 'Physical Therapy (₱1,200)'),
    ]
    
    patient_name = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='checkup')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.patient_name} - {self.service_type} ({self.status})"