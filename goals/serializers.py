from rest_framework import serializers

from goals.models import Goal, GoalMetrics

from appointments.models import Appointment
from django.utils.translation import gettext as _


class GoalSerializer(serializers.ModelSerializer):
    # serializer principal de la app goals, convierte el modelo Goal a Json
    # si se elimina la app goals, este serializer completo debe eliminarse

    class Meta:
        model = Goal
        fields = '__all__'

    def validate(self, data):
        # aqui se validan las fechas antes de guardar una meta nueva

        # verifica que la fecha de fin no sea anterior a la de inicio
        if data['start_time'] > data['end_time']:
            raise serializers.ValidationError({"message": "End date must occur after start date"})

        # verifica que no exista ya una meta que cubra el mismo rango de fechas
        already_goal = Goal.objects.filter(
            start_time__lte=data['start_time'],
            end_time__gte=data['end_time']
        ).exists()

        if already_goal:
            raise serializers.ValidationError({"message": "A Goal already exists within this date range"})

        # verifica que no exista otra meta con la misma fecha de inicio
        already_goal_start = Goal.objects.filter(
            start_time__gte=data['start_time'],
        ).exists()

        if already_goal_start:
            raise serializers.ValidationError({"message": "A Goal already exists within this start range"})

        # verifica que no exista otra meta con la misma fecha de fin
        already_goal_end = Goal.objects.filter(
            end_time__gte=data['end_time']
        ).exists()

        if already_goal_end:
            raise serializers.ValidationError({"message": "A Goal already exists within this end range"})

        return data

    # def validate_start_time(self, start_time):
    #     already_Goal = Goal.objects.filter(start_time__lte = start_time).exists()

    #     if already_Goal:
    #         raise serializers.ValidationError(
    #             _('A Goal already has this date'))

    #     return super().validate_start_time(start_time)

    # def validate_end_time(self, end_time):
    #     already_Goal = Goal.objects.filter(end_time__gte = end_time).exists()

    #     if already_Goal:
    #         raise serializers.ValidationError(
    #             _('A Goal already has this date'))

    #     return super().validate_end_time(end_time)

    def save(self, **kwargs):
        # aqui se guarda la meta y se intenta obtener la mas reciente
        goal = super().save(**kwargs)
        try:
            set_goal = Goal.objects.latest('created_at')
            # aqui se obtiene la meta mas recientemente creada
            goal_appointments = Appointment.objects.filter(goal=set_goal.pk)
            # aqui se cuentan las citas asociadas a esa meta
            #GoalMetrics.objects.create(appointments = goal_appointments.count(), monthly_goal_porcentage = goal_appointments.count()/set_goal.apponitments_goal, assistance =goal_appointments.filter(status="DONE").count())
            # esta linea esta comentada: era la creacion de GoalMetrics en base de datos, ahora se calcula en vivo
        except Goal.DoesNotExist:
            pass
        return goal


class GoalMetricsSerializer(serializers.ModelSerializer):
    # serializer para las metricas calculadas de una meta
    # GoalMetrics no se guarda en base de datos, solo se serializa para devolverlo en la respuesta
    # si se elimina la app goals, este serializer completo debe eliminarse

    class Meta:
        model = GoalMetrics
        fields = '__all__'