from django.shortcuts import render, get_object_or_404, redirect
from doctor.models import users_class, Patient, MedicalRecord, Doctor, MedicalReportRequest


def patient_homepage(request):
    user_id = request.session.get('user_id')
    doctors = Doctor.objects.all()
    medical_report_request_doctors = MedicalReportRequest.objects.filter(patient__user__id=user_id)
    print(medical_report_request_doctors)

    context = {
        'doctors':                        doctors,
        'medical_report_request_doctors': medical_report_request_doctors,
    }
    return render(request, 'patient_dashboard.html', context)


def patient_add_profile(request):
    error_message = None

    if request.method == 'POST':
        user_id = request.session['user_id']

        user_instance = users_class.objects.get(pk=user_id)

        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        # Check if a Patient instance already exists for the user
        patient, created = Patient.objects.get_or_create(user=user_instance)

        # If Patient instance already exists, update its fields
        if not created:
            patient.phone_number = phone_number
            patient.date_of_birth = date_of_birth
            patient.address = address
            patient.gender = gender
            patient.save()

            error_message = "Profile Updated Successfully"
        else:
            error_message = "Error: No existing Patient profile found for the user."

    return render(request, 'add_profile.html', {'error_message': error_message})


def add_medical_record(request):
    error_message = None

    if request.method == 'POST':
        # Get the user_id from the session
        user_id = request.session.get('user_id')

        # Retrieve the patient associated with the user_id
        patient = get_object_or_404(Patient, user__id=user_id)
        print(patient, '-------------------------------------------')

        blood_group = request.POST.get('blood_group')
        symptoms = request.POST.get('symptoms')

        # Create a new MedicalRecord instance and associate it with the patient
        medical_record = MedicalRecord.objects.create(
            patient=patient,
            blood_group=blood_group,
            symptoms=symptoms
        )

        # Handle file upload for the image
        image = request.FILES.get('image')
        if image:
            medical_record.image = image
            medical_record.save()

    return render(request, 'add_medical_record.html')


def doctor_view_list(request):
    user_id = request.session.get('user_id')

    doctors = Doctor.objects.all()

    context = {
        'doctors': doctors,
    }
    return render(request, 'doctors_list.html', context)


def patient_accept_reject(request, action, medical_id):
    medical = MedicalReportRequest.objects.filter(id=medical_id).update(status=action)
    print(action, medical_id, medical)
    return redirect('patient_home')


def view_medical_record(request):
    user_id = request.session.get('user_id')
    patient = MedicalReportRequest.objects.filter(patient__user__id=user_id)
    print(patient)
    context = {
        'patient': patient,
    }
    return render(request, 'view_medical_record.html', context)
