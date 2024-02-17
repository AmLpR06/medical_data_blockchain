from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
import re
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from web3 import Web3
from doctor.models import users_class, Doctor, Patient, MedicalReportRequest, MedicalRecord
from doctor.web3_file import add_user_to_blockchain, get_user

"""
-----------------------------------------------Authentication functions-------------------------------------------------
"""



def validate_password(password):
    # Minimum 6 characters, maximum 15 characters
    if not 6 <= len(password) <= 15:
        raise ValidationError("Password must be between 6 and 15 characters.")

    # At least one uppercase letter
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")

    # At least one digit
    if not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one digit.")

    # At least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character.")

    return password


def sign_in(request):
    error_message = None  # Initialize error message

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the provided email exists
        if users_class.objects.filter(email=email).exists():
            user = users_class.objects.get(email=email)
            query_password = user.password  # Retrieve hashed password from the database
            role = user.role

            # Verify the hashed password against the provided password
            if check_password(password, query_password):
                if role == 'doctor':
                    request.session['user_id'] = user.id
                    return redirect('doctor_home')
                elif role == 'patient':
                    request.session['user_id'] = user.id
                    user_mail =  user.email
                    user_datail = get_user(user_mail)
                    if user_datail:
                        return redirect('patient_home')
                else:
                        return redirect('sign_in')
            else:
                error_message = "Invalid password. Please try again."
        else:
            error_message = "Invalid username or password. Please try again."
    

    return render(request, 'login.html', {'error_message': error_message})



def sign_up(request):
    error_message = None  # Initialize error message

    if request.method == 'POST':
        # Retrieve form data from the POST request
        username = request.POST.get('username')
        role = request.POST.get('role')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the provided username or email already exists
        if users_class.objects.filter(username=username).exists() or users_class.objects.filter(email=email).exists():
            error_message = "A user with this username or email already exists. Please choose a different one."
        else:
            # Validate the password
            try:
                validate_password(password)
            except ValidationError as e:
                error_message = str(e)

            if not error_message:
                hashed_password = make_password(password)

               
                # tx_receipt = add_user_to_blockchain(username, hashed_password, email)


                # if tx_receipt:
                
                    # If the transaction succeeds, create a new user instance and save it to the database
                user = users_class.objects.create(username=username, email=email, password=hashed_password,
                                                        role=role)
                    # print(tx_receipt, '*************************')
                if role == 'doctor':
                    Doctor.objects.create(
                        user=user,
                        phone_number=None,
                        medical_license_number=None,
                        gender=None
                    )
                else:
                    Patient.objects.create(
                        user=user,
                        date_of_birth=None,
                        address=None,
                        gender=None,
                        phone_number=None,
                    )
            
        
                # Store hashed user data on the blockchain
                

                # Process the transaction receipt or return some response
                
                    # Redirect to a success page or homepage
                return redirect('sign_in')

    # Pass the error message to the template
    return render(request, 'registration.html', {'error_message': error_message})


def logout(request):
    # Clear user-related session data
    if 'user_id' in request.session:
        del request.session['user_id']

    # Add any other session data clearing logic if needed

    # Redirect to the home page or login page after signout
    return redirect('sign_in')  # Replace 'home' with the name of your home or login URL


"""
-----------------------------------------------Main functions-----------------------------------------------------------
"""


def doctor_homepage(request):
    user_id = request.session['user_id']

    # Get today's date
    today = timezone.now().date()
    # Filter users created today
    users_today = users_class.objects.filter(created_at__date=today)
    total_users_count = users_class.objects.count()
    today_users_count = users_today.count()

    users = users_class.objects.all()
    medical_report_request_patients = MedicalReportRequest.objects.filter(requested_by__user__id=user_id)
    medical_report_request_accepted = MedicalReportRequest.objects.filter(requested_by__user__id=user_id,
                                                                          status='accepted')

    print(medical_report_request_accepted.count())
    context = {
        'total_users_count':               total_users_count,
        'today_users_count':               today_users_count,
        'users':                           users,
        'medical_report_request_patients': medical_report_request_patients,
        'medical_report_request_accepted': medical_report_request_accepted.count(),
    }
    return render(request, 'dashboard.html', context)


def patients_view_list(request):
    user_id = request.session.get('user_id')

    patients = Patient.objects.all()

    context = {
        'patients': patients,
    }
    return render(request, 'patients_list.html', context)


def doctor_add_profile(request):
    error_message = None

    if request.method == 'POST':
        user_id = request.session['user_id']

        user_instance = users_class.objects.get(pk=user_id)
        print(type(user_instance), '*********')

        phone_number = request.POST.get('phone_number')
        medical_license_number = request.POST.get('medical_license_number')
        gender = request.POST.get('gender')

        # Check if a Doctor instance already exists for the user
        doctor, created = Doctor.objects.get_or_create(user=user_instance)

        # If Doctor instance already exists, update its fields
        if not created:
            doctor.phone_number = phone_number
            doctor.medical_license_number = medical_license_number
            doctor.gender = gender
            doctor.save()

            error_message = "Profile Updated Successfully"
        else:
            error_message = "Error: No existing Doctor profile found for the user."

    return render(request, 'doctor_profile_add.html', {'error_message': error_message})


def request_view_medical_record(request, patient_id):
    user_id = request.session.get('user_id')
    patient = Patient.objects.filter(user__id=patient_id).first()
    doctor = Doctor.objects.filter(user__id=user_id).first()
    medical_data = MedicalRecord.objects.filter(patient__user__id=patient_id).first()
    print(type(patient))
    MedicalReportRequest.objects.create(
        patient=patient, requested_by=doctor, medical_data=medical_data,
    )
    return redirect('patients_view_list')


def view_accepted_medical_records(request, patients_id):
    patient = MedicalReportRequest.objects.filter(id=patients_id)
    print(patient)
    context = {
        'patient': patient,
    }

    if request.method == 'POST':
        doctor_note = request.POST.get('doctor_note')
        prescription = request.POST.get('prescription')
        diagnosis = request.POST.get('diagnosis')
        print(doctor_note, prescription, diagnosis)
        MedicalRecord.objects.filter(id=patients_id).update(doctor_note=doctor_note, diagnosis=diagnosis,
                                                            prescription=prescription)

    return render(request, 'view_single_person_medical.html', context)


    