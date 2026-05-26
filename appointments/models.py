from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

class Appointment(models.Model):

    class StatusType(models.TextChoices):
        #qui se crean opciones sobre el estado de la citas
        DONE = 'DONE', _('Hecho')
        PENDING = 'PENDING', _('Pendiente')
        CANCELLED = 'CANCELLED', _('Cancelado')
    class PlaceType(models.TextChoices):
        #aqui se crea opciones sobre el establecimiento donde se hara la cita
        CDO = 'CDO', _('CDO')
        SEMILLERO = 'SEMILLERO', _('Semillero')
        OTHER = 'OTHER', _('Otro')

    patient = models.ForeignKey(
        # Paciente al que pertenece la cita
# PROTECT evita que se elimine un paciente si tiene citas registradas
        'patient.Patient',
        on_delete=models.PROTECT,
        related_name='appointment'
    )
    place = models.CharField(
        # Lugar donde se realizará la cita
# max_length limita el texto a 50 caracteres
# choices restringe los valores permitidos a los definidos en Pla
        max_length=50,
        choices=PlaceType.choices,
        default=PlaceType.CDO
    )
    
# Notas adicionales sobre la cita
# TextField permite guardar texto largo sin límite de caracteres
    notes = models.TextField()
    

    # created_by = models.ForeignKey(
    #     get_user_model(),
    #     on_delete=models.PROTECT,
    #     related_name='appointment'
    # )
    doctor = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='appointment'
    )
    hour = models.TimeField()
    date = models.DateField()
    # campo que conecta cada cita con la meta activa al momento de crearla
    # este campo es el enlace principal entre appointments y goals
    # si se elimina la app goals, este campo debe eliminarse del modelo
    goal = models.ForeignKey(
        'goals.Goal',
        # apunta al modelo Goal de la app goals
        on_delete=models.PROTECT,
        # PROTECT evita eliminar una meta si tiene citas asociadas
        related_name='goal',
        blank=True,
        null=True,
        # es opcional: una cita puede existir sin meta asignada
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=50,
        choices=StatusType.choices,
        default=StatusType.PENDING)

    def __str__(self):
        return f'{self.date} - {self.patient} - {self.doctor}'