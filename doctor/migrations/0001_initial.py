# Generated by Django 4.2.8 on 2023-12-08 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users_class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('role', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='doctor.users_class')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_group', models.CharField(blank=True, max_length=5, null=True)),
                ('doctor_note', models.TextField(blank=True, null=True)),
                ('diagnosis', models.TextField(blank=True, null=True)),
                ('prescription', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('symptoms', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='medical_records/')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('medical_license_number', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='doctor.users_class')),
            ],
        ),
    ]
