from rest_framework import serializers
from .models import Facility, ServiceType, Patient

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id', 'name', 'location', 'created_at']

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['id', 'name', 'description']

class PatientSerializer(serializers.ModelSerializer):
    mrn = serializers.CharField(read_only=True)
    facility = FacilitySerializer(read_only=True)
    facility_id = serializers.PrimaryKeyRelatedField(
        queryset=Facility.objects.all(), source='facility', write_only=True
    )
    services = ServiceTypeSerializer(many=True, read_only=True)
    service_ids = serializers.PrimaryKeyRelatedField(
        queryset=ServiceType.objects.all(), many=True, source='services', write_only=True
    )
    
    class Meta:
        model = Patient
        fields = [
            'id', 'mrn', 'first_name', 'last_name', 'gender', 'date_of_birth',
            'phone', 'email', 'address', 'insurance_provider', 'insurance_number',
            'facility', 'facility_id', 'services', 'service_ids', 'created_at', 'updated_at'
        ]
