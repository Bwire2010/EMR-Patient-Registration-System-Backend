from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FacilityViewSet, ServiceTypeViewSet, PatientViewSet, custom_token_view

router = DefaultRouter()
router.register(r'facilities', FacilityViewSet)
router.register(r'services', ServiceTypeViewSet)
router.register(r'patients', PatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
     path('token/', custom_token_view),
]