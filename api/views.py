from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group

from .models import *
from .serializer import *

# Create your views here.

#------------------------------------------------------------login views -----------------------------------------------------------------

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def obtain_token(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=400)

    token, created = Token.objects.get_or_create(user=user)
    
    groups = user.groups.all()
    group_names = [group.name for group in groups]

    return Response({'token': token.key, 'role': group_names[0]})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def verify_token(request):
    return Response({'detail': 'Token is valid'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    user = request.user
    serializer = UserDetailsSerializer(user)
    data = serializer.data
    return Response(data)

#----------------------------------------------------------display GET views------------------------------------------------------------

@api_view(['GET'])
@permission_classes([])
def apiOverview(request):
    api_urls = {
        'Doctors List': '/doctors/',
        'Patients List': '/patients/',
        'Appointments List': '/appointments/',
        'Departments List': '/departments/',
        'Department Doctors List': '/departments/<str:pk>/doctors/',
        'Department Patients List': '/departments/<str:pk>/patients/',
        "Doctors Info": '/doctors/<str:pk>/',
        'Doctors Appointment List': '/doctors/<str:pk>/appointments/',
        "Patients Info": '/patients/<str:pk>/',
        'Patients Appointment List': '/patients/<str:pk>/appointments/',
        'Create': '/task-create/',
        'Update': '/task-update/<str: pk>/',
        'Delete': '/task-delete/<str: pk>/',
    }
    return Response(api_urls)


@api_view(['GET'])
@permission_classes([])
def adminsList(request):
    admins = Admin.objects.all()
    serializer = AdminSerializer(admins, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def doctorsList(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def patientsList(request):
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def departmentsList(request):
    dept = Department.objects.all()
    serializer = DepartmentSerializer(dept, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getDepartmentDoctors(request, pk):
    doctors = Doctor.objects.filter(Department=pk)
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def appointmentsList(request):
    appointments = Appointment.objects.all()
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getDoctorsInfo(request, pk):
    doctor = Doctor.objects.get(id=pk)
    department_name = doctor.Department.name
    serializer = DoctorSerializer(
        doctor, context={'department_name': department_name})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getDoctorsAppointments(request, pk):
    appointments = Appointment.objects.filter(Doctor=pk)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getPatientsInfo(request, pk):
    patient = Patient.objects.get(id=pk)
    serializer = PatientSerializer(patient)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getPatientsAppointments(request, pk):
    appointments = Appointment.objects.filter(Patient=pk)
    doctor_name = appointments[0].Doctor.name
    patient_name = appointments[0].Patient.name
    department_name = appointments[0].Department.name
    serializer = AppointmentSerializer(appointments, context={
        'doctor_name': doctor_name,
        'patient_name': patient_name,
        'department_name': department_name
    }, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getAdminsInfo(request, pk):
    admin = Admin.objects.get(id=pk)
    serializer = AdminSerializer(admin)
    return Response(serializer.data)

#---------------------------------------------------------------Add POST views-----------------------------------------------------------

@api_view(['POST'])
@permission_classes([])
def addAppointment(request):
    serializer = AddAppointmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([])
def addDoctor(request):
    data = request.data
    department_id = data.pop('department_id')
    department = Department.objects.get(id=department_id)
    
    username = data['name'].replace(" ", "").lower()
    password = data.pop('password', 'hospitaluser')
    user = User.objects.create_user(username=username, password=password)
    user.groups.add(doctor)
    user.save()

    doctor = Doctor.objects.create(user=user, Department=department, **data)

    serializer = DoctorSerializer(doctor)
    return Response(serializer.data, status=201)


#---------------------------------------------------------------Update PUT views-----------------------------------------------------------

@api_view(['PUT'])
@permission_classes([])
def completeAppointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        if appointment.status == 'Scheduled':
            appointment.status = 'Completed'
            appointment.save()
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data)
        else:
            return Response({'error': 'Appointment status cannot be updated.'}, status=400)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found.'}, status=404)