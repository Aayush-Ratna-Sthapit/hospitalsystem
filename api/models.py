from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    Department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
class Patient(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    age = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed')
    )

    id = models.IntegerField(primary_key=True)
    Doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL)
    Patient = models.ForeignKey(Patient, null=True, on_delete=models.SET_NULL)
    Department = models.ForeignKey(Department,null=True, on_delete=models.SET_NULL)
    date = models.DateField(null=True, auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=50, null=True, choices=STATUS)
    

class Admin(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=200, null=True, default='Admin')
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name