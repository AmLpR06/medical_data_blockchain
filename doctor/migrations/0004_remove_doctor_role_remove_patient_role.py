# Generated by Django 4.2.8 on 2023-12-08 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_users_class_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='role',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='role',
        ),
    ]
