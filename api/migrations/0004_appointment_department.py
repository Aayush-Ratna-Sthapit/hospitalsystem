# Generated by Django 4.2.2 on 2023-07-08 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_appointment_app_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="department",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.department",
            ),
        ),
    ]
