# Create your models here.
from django.db import models
import string
import random
from django.utils import timezone

class Facility(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name

class ServiceType(models.Model):
    name = models.CharField(max_length=100)  # e.g., Lab, Radiology
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

def generate_mrn(facility_code):
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{facility_code}-{random_part}"


class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    mrn = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    insurance_provider = models.CharField(max_length=100, blank=True)
    insurance_number = models.CharField(max_length=50, blank=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='patients')
    services = models.ManyToManyField(ServiceType, related_name='patients')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['mrn']),
            models.Index(fields=['last_name', 'first_name']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.mrn})"

    def save(self, *args, **kwargs):
        # Generate MRN only if it doesn't already exist
        if not self.mrn and self.facility:
            # Use the first 3 letters of facility name, uppercased
            facility_code = self.facility.name[:3].upper()
            new_mrn = generate_mrn(facility_code)

            # Ensure uniqueness in the DB
            while Patient.objects.filter(mrn=new_mrn).exists():
                new_mrn = generate_mrn(facility_code)

            self.mrn = new_mrn

        super().save(*args, **kwargs)