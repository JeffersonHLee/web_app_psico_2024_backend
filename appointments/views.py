from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from appointments.models import Appointment
from appointments.serializers import AppointmentReadSerializer, AppointmentSerializer
from django.utils.timezone import now
from goals.models import Goal
# se importa Goal para buscar la meta activa al momento de crear una cita
# si se elimina la app goals, este import debe eliminarse
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED


class AppointmentCreateApiView(ListCreateAPIView):
    #aqui se crea una lista sobre las citas
    queryset = Appointment.objects.all()
    #aqui trae todas las citas crreadas
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    # def get_queryset(self):
    #     return Appointment.objects.filter(doctor=self.request.user.pk)

    def post(self, request: Request, format=None, *args, **kwargs):
        # el metodo post fue reescrito manualmente para poder inyectar la meta activa automaticamente
        # si se elimina goals, este metodo puede simplificarse usando perform_create normal
        try:
            set_goal = Goal.objects.get(start_time__lte=now().date(), end_time__gte=now().date())
            #aqui se obtiene las metas(goals) creadas segun su tiempo y fecha ademas de cuando finalizan
        except Goal.DoesNotExist:
            #excepto cuando la meta(goal) no existe da el mensaje de meta no establecida y su caracteristico error 404 not found
            # si se elimina goals, este bloque try/except completo debe eliminarse
            return Response(
                {'message': 'No set goal'},
                status=HTTP_404_NOT_FOUND
            )

        serializer_class = self.get_serializer_class()

        serializer = serializer_class(data={
            'goal': set_goal.pk,
            # aqui se inyecta el id de la meta activa en los datos de la cita
            # si se elimina goals, esta linea debe eliminarse
            'patient': request.data.get('patient'),
            'doctor': request.data.get('doctor'),
            'hour': request.data.get('hour'),
            'date': request.data.get('date'),
            'status': request.data.get('status'),
            'place': request.data.get('place'),
            'notes': request.data.get("notes")
        })

        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()
        appointment_data = self.get_serializer(appointment).data

        return Response(appointment_data, status=HTTP_201_CREATED)
    
    # def perform_create(self, serializer):
    #     try:
    #         set_goal = Goal.objects.get(startTime__lte = now().date(), endTime__gte = now().date())
    #         serializer.validated_data['goal'] = set_goal
    #         serializer.save()
    #     except exceptions.ObjectDoesNotExist:
    #         print("entro al except")
    #         return Response(
    #             {'message': 'No set goal'},
    #             status=HTTP_404_NOT_FOUND
    #         )

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