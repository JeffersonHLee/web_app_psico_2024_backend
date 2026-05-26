from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from patient.models import Patient
from patient.serializers import PatientSerializer
from rest_framework import filters

class PatientCreateApiView(ListCreateAPIView):
    # Vista para listar y crear pacientes
    queryset = Patient.objects.all()
    # aqui trae todos los pacientes registrados
    serializer_class = PatientSerializer
    # aqui se convierte la informacion del paciente a Json
    permission_classes = [IsAuthenticated]
    # aqui se autentica para que solo usuarios registrados puedan acceder

class PatientRetrieveApiView(RetrieveUpdateAPIView):
    # Vista para obtener y actualizar un paciente especifico por su id
    queryset = Patient.objects.all()
    # aqui trae todos los pacientes para buscar el que se necesita
    serializer_class = PatientSerializer
    # aqui se convierte la informacion a Json
    permission_classes = [IsAuthenticated]
    # aqui se autentica para que solo usuarios registrados puedan acceder

class PatientListApiView(ListAPIView):
    # Vista para listar pacientes con busqueda por nombre
    queryset = Patient.objects.all()
    # aqui trae todos los pacientes registrados
    serializer_class = PatientSerializer
    # aqui se convierte la informacion a Json
    permission_classes = [IsAuthenticated]
    # aqui se autentica para que solo usuarios registrados puedan acceder
    filter_backends = [filters.SearchFilter]
    # aqui se agrega el filtro de busqueda
    search_fields=["name"]
    # aqui se indica que el campo de busqueda es el nombre del paciente

