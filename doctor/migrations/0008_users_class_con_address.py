# Generated by Django 4.2.8 on 2024-02-17 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0007_alter_medicalreportrequest_requested_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='users_class',
            name='con_address',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
