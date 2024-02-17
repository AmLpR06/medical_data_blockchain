from django.db import models


class users_class(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=28, null=True)
    con_address=models.CharField(max_length=30, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.username


class Patient(models.Model):
    user = models.OneToOneField(users_class, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
                              null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username if self.user else 'No User'


class Doctor(models.Model):
    user = models.OneToOneField(users_class, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    medical_license_number = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
                              null=True, blank=True)

    def __str__(self):
        return self.user.username if self.user else 'No User'


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5, null=True, blank=True)
    doctor_note = models.TextField(null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    prescription = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    symptoms = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='medical_records/', null=True, blank=True)

    def __str__(self):
        return f'Medical Record for {self.patient.user.username}' if self.patient else 'No Patient'


class MedicalReportRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True, null=True)
    requested_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medical_data = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Medical Report Request for {self.patient.user.username}' if self.patient else 'No Patient'
