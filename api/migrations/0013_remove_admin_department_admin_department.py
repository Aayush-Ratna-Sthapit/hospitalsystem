# Generated by Django 4.2.2 on 2023-07-20 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0012_admin_user_doctor_user_patient_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="admin",
            name="Department",
        ),
        migrations.AddField(
            model_name="admin",
            name="department",
            field=models.CharField(default="Admin", max_length=200, null=True),
        ),
    ]
