from django.contrib import admin
from .models import Facility, ServiceType, Patient


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at')
    search_fields = ('name', 'location')


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('mrn', 'first_name', 'last_name', 'gender', 'facility', 'created_at')
    search_fields = ('mrn', 'first_name', 'last_name')
    list_filter = ('gender', 'facility', 'services')
    filter_horizontal = ('services',)  # Makes selecting many-to-many easier
