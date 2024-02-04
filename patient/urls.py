from django.urls import path
from patient.views import patient_homepage, patient_add_profile, add_medical_record, doctor_view_list, \
    view_medical_record, patient_accept_reject

urlpatterns = [

    path('', patient_homepage, name='patient_home'),
    path('patient_add_profile', patient_add_profile, name='patient_add_profile'),
    path('add_medical_record', add_medical_record, name='add_medical_record'),
    path('doctor_view_list', doctor_view_list, name='doctor_view_list'),
    path('patient_accept_reject/<str:action>/<int:medical_id>/', patient_accept_reject, name='patient_accept_reject'),
    path('view_medical_record', view_medical_record, name='view_medical_record'),
]
