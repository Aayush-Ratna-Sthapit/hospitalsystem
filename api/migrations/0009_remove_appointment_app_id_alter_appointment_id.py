# Generated by Django 4.2.2 on 2023-07-09 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_remove_doctor_d_id_remove_patient_p_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="appointment",
            name="app_id",
        ),
        migrations.AlterField(
            model_name="appointment",
            name="id",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]