from django.urls import path


from patient.views import (
    PatientCreateApiView,
    PatientRetrieveApiView,
    PatientListApiView,
)

urlpatterns = [
    path('',
         PatientCreateApiView.as_view(),
         name='patient-create'),
    # ruta para listar y crear pacientes: GET /api/v1/patient/  POST /api/v1/patient/
    path('<int:pk>/',
         PatientRetrieveApiView.as_view(), name='patient-detail'),
    # ruta para ver o editar un paciente especifico: GET/PATCH /api/v1/patient/<id>/
    path('list/', PatientListApiView.as_view(), name='patient-list'),
    # ruta para buscar pacientes por nombre: GET /api/v1/patient/list/?search=nombre
]
