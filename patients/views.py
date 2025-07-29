from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # ✅ Add this
from django.db import models
from .models import Facility, ServiceType, Patient
from .serializers import FacilitySerializer, ServiceTypeSerializer, PatientSerializer


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    # permission_classes = [IsAuthenticated]

class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    # permission_classes = [IsAuthenticated]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    # permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            patients = self.queryset.filter(
                models.Q(mrn__icontains=query) |
                models.Q(first_name__icontains=query) |
                models.Q(last_name__icontains=query)
            )
        else:
            patients = self.queryset
        serializer = self.get_serializer(patients, many=True)
        return Response(serializer.data)
