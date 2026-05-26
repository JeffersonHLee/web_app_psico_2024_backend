from django.db import models

class Goal(models.Model):
    # modelo que representa una meta de citas para un periodo de tiempo
    created_at = models.DateTimeField(auto_now_add=True)
    # fecha en que se creo la meta, se agrega automaticamente
    updated_at = models.DateTimeField(auto_now=True)
    # fecha de la ultima actualizacion, se actualiza automaticamente
    start_time = models.DateField()
    # fecha de inicio del periodo de la meta
    end_time = models.DateField()
    # fecha de fin del periodo de la meta
    apponitments_goal = models.IntegerField()
    # numero de citas que se quieren alcanzar en el periodo

    def __str__(self):
        return f'{self.start_time} - {self.end_time} - {self.pk}'

class GoalMetrics(models.Model):
    # modelo para representar las metricas calculadas de una meta, no se guarda en la base de datos
    appointments = models.IntegerField()
    # total de citas registradas en el periodo de la meta
    monthly_goal_porcentage = models.FloatField()
    # porcentaje de avance respecto a la meta de citas
    assistance = models.IntegerField()
    # total de citas con estado DONE (asistidas)
    totalAppointments = models.IntegerField()
    # numero de citas objetivo de la meta

    def __str__(self):
        return f'{self.appointments} - {self.monthly_goal_porcentage} - {self.assistance}'
