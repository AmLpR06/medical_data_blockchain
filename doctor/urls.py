from django.urls import path
from doctor.views import doctor_homepage, patients_view_list, doctor_add_profile, request_view_medical_record, \
    view_accepted_medical_records

urlpatterns = [

    path('', doctor_homepage, name='doctor_home'),
    path('patients_view_list', patients_view_list, name='patients_view_list'),
    path('doctor_add_profile', doctor_add_profile, name='doctor_add_profile'),
    path('request_view_medical_record/<int:patient_id>/', request_view_medical_record,
         name='request_view_medical_record'),
    path('view_accepted_medical_records/<int:patients_id>/', view_accepted_medical_records,
         name='view_accepted_medical_records'),

]
