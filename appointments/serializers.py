from rest_framework import serializers

from appointments.models import Appointment

from patient.serializers import PatientSerializer

from psico_auth.serializer import UserSerializer

from goals.serializers import GoalSerializer
# se importa GoalSerializer para poder mostrar el detalle de la meta dentro de una cita
# si se elimina la app goals, este import debe eliminarse


class AppointmentSerializer(serializers.ModelSerializer):
    # created_by = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )

    #goal = GoalSerializer(required=False)


    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentReadSerializer(AppointmentSerializer):
    patient = PatientSerializer()
    doctor = UserSerializer()
    goal = GoalSerializer()
    # aqui se anida el detalle completo de la meta dentro de la respuesta de la cita
    # si se elimina la app goals, esta linea debe eliminarse
    # created_by = UserSerializer()
