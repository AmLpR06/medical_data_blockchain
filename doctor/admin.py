from django.contrib import admin
from doctor.models import users_class, Patient, Doctor, MedicalRecord, MedicalReportRequest
from django.contrib.auth.models import Group

admin.site.register(users_class)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(MedicalRecord)
admin.site.register(MedicalReportRequest)


# Create a custom admin class for the Group model
class GroupAdmin(admin.ModelAdmin):
    pass


# Unregister the Group model from the admin site
admin.site.unregister(Group)
