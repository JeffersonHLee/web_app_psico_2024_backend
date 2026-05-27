from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from appointments.models import Appointment
from appointments.serializers import AppointmentReadSerializer, AppointmentSerializer
from django.utils.timezone import now


class AppointmentCreateApiView(ListCreateAPIView):
    #aqui se crea una lista sobre las citas
    queryset = Appointment.objects.all()
    #aqui trae todas las citas creadas
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

class AppointmentRetrieveApiView(RetrieveUpdateAPIView):
    # Vista para obtener y actualizar una cita especifica por su id
    queryset = Appointment.objects.all()
    # aqui trae todas las citas para buscar la que se necesita

    def get_serializer_class(self):
        # aqui se decide que serializer usar segun el tipo de peticion
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return AppointmentSerializer
            # si es una actualizacion se usa el serializer de escritura
        return AppointmentReadSerializer
        # si es una lectura se usa el serializer de solo lectura
    permission_classes = [IsAuthenticated]
    # aqui se autentica para que solo usuarios registrados puedan acceder
    
class AppointmentGetPendingApiView(ListAPIView):
    today = now().date()
    queryset = Appointment.objects.filter(date__gte=today, status="PENDING").order_by('date')
    #filta las citas por fecha, hora, estatus y ordena por fecha
    serializer_class = AppointmentReadSerializer
    permission_classes = [IsAuthenticated]
    # def get_queryset(self):
    #     return Appointment.objects.filter(doctor=self.request.user.pk)