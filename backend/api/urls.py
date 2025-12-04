from django.urls import path
from . import views

urlpatterns = [
    path('request-medical-records', views.request_medical_records),
    path('covid19-consent-form', views.covid19_consent_form),
    path('apply-for-patient-assistance', views.apply_for_patient_assistance),
    path('extensions', views.get_extension_apps),
]
