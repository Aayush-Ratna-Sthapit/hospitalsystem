from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import *

class DoctorSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='Department.name', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'Department', 'department_name', 'phone', 'email']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='Doctor.name', read_only=True)
    patient_name = serializers.CharField(source='Patient.name', read_only=True)
    department_name = serializers.CharField(source='Department.name', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'Doctor', 'Patient', 'Department', 'department_name', 'date', 'status', 'doctor_name', 'patient_name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class UserDetailsSerializer(serializers.ModelSerializer):
    user_groups = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    def get_user_id(self, user):
        if user.groups.filter(name='doctor').exists():
            return user.doctor.id if hasattr(user, 'doctor') else None
        elif user.groups.filter(name='patient').exists():
            return user.patient.id if hasattr(user, 'patient') else None
        elif user.groups.filter(name='admin').exists():
            return user.admin.id if hasattr(user, 'admin') else None
        else:
            return None

    def get_user_groups(self, user):
        return user.groups.first().name if user.groups.exists() else None

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_id', 'user_groups']
        extra_kwargs = {'id': {'read_only': True}, 'user_groups': {'read_only': True}, 'user_id': {'read_only': True}}

class AddAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        exclude = ['id']

class AddDoctorSerializer(serializers.ModelSerializer):
    Department = DepartmentSerializer()
    
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'Department', 'phone', 'email']