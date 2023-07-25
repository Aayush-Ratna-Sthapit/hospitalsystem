from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='apiOverview'),

    path('doctors/', views.doctorsList, name='doctors'),
    path('doctors/<str:pk>/', views.getDoctorsInfo, name='doctors-info'),

    path('patients/', views.patientsList, name='patients'),
    path('patients/<str:pk>/', views.getPatientsInfo, name='patients-info'),

    path('admins/', views.adminsList, name='admins'),
    path('admins/<str:pk>/', views.getAdminsInfo, name='admins-info'),

    path('departments/', views.departmentsList, name='departments'),
    path('departments/<str:pk>/', views.getDepartmentDoctors, name='department-doctors'),

    path('appointments/', views.appointmentsList, name='appointments'),
    path('doctors/<str:pk>/appointments/', views.getDoctorsAppointments, name='doctors-appointments'),
    path('patients/<str:pk>/appointments/', views.getPatientsAppointments, name='patients-appointments'),
    path('appointments/add/', views.addAppointment, name='add-appointment'),
    path('appointments/<int:appointment_id>/complete/', views.completeAppointment, name='complete-appointment'),

    path('token/', views.obtain_token, name='token_obtain'),
    path('token/verify/', views.verify_token, name='token_verify'),
    path('user/details/', views.user_details, name='user-details'),
]