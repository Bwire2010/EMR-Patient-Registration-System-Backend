from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from django.db import models
from .models import Facility, ServiceType, Patient
from .serializers import FacilitySerializer, ServiceTypeSerializer, PatientSerializer
from oauth2_provider.models import Application
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
def custom_token_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=400)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=401)

    # Get the first available OAuth2 application
    try:
        app = Application.objects.filter(authorization_grant_type='password').first()
        if not app:
            raise Application.DoesNotExist()
    except Application.DoesNotExist:
        return Response({'error': 'OAuth application not found'}, status=500)

    # Build the token URL dynamically
    token_url = request.build_absolute_uri('/o/token/')

    payload = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': app.client_id,
        'client_secret': app.client_secret,
    }

    response = requests.post(token_url, data=payload)
    return Response(response.json(), status=response.status_code)




class NoPagination(PageNumberPagination):
    page_size = None

class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NoPagination

class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NoPagination 


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({
                "status": True,
                "message": "Patient successfully registered.",
                "data": serializer.data,
                "code": 201
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({
                "status": False,
                "message": "Validation error.",
                "errors": e.detail,
                "code": 400
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({
                "status": False,
                "message": "An unexpected error occurred. Please try again later.",
                "code": 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                "status": True,
                "message": "Patient details updated successfully.",
                "data": serializer.data,
                "code": 200
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({
                "status": False,
                "message": "Validation error.",
                "errors": e.detail,
                "code": 400
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({
                "status": False,
                "message": "An unexpected error occurred. Please try again later.",
                "code": 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                "status": True,
                "message": "Patient deleted successfully.",
                "code": 200
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "status": False,
                "message": "An unexpected error occurred. Please try again later.",
                "code": 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                "status": True,
                "message": "Patient details retrieved successfully.",
                "data": serializer.data,
                "code": 200
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                "status": False,
                "message": "Patient not found.",
                "code": 404
            }, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            # Ensure ordering by latest
            queryset = queryset.order_by('-created_at')

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "status": True,
                "message": "Patients retrieved successfully.",
                "data": serializer.data,
                "code": 200
            })

        except Exception as e:
            print("ERROR:", e)
            return Response({
                "status": False,
                "message": "An unexpected error occurred. Please try again later.",
                "code": 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def search(self, request, *args, **kwargs):
        query = request.query_params.get("q", "")
        queryset = self.get_queryset().filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(mrn__icontains=query)
        ).order_by('-created_at')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "message": "Search completed successfully.",
            "data": serializer.data,
            "code": 200
        })

