from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

class Activity(models.Model):


    class StatusType(models.TextChoices):
        # aqui se utiliza el TextChoices para distintas opciones las cuales se especifica despues del doble punto dandole el nombre y dentro aplicandole la traduccion deseada
        DONE = 'DONE', _('Hecho')
        PENDING = 'PENDING', _('Pendiente')
        CANCELLED = 'CANCELLED', _('Cancelado')

    class PlaceType(models.TextChoices):
        # aqui se  vuelve a utilizar un TextChoices para la ubicacion de la actividad
        CDO = 'CDO', _('CDO')
        SEMILLERO = 'SEMILLERO', _('Semillero')
        OTHER = 'OTHER', _('Otro')

    doctors = models.ManyToManyField(
        #aqui se toma a un usuario creado(doctor) para agregarlo como participese de la actividad
        get_user_model(),
        related_name='activity'
    )#aqui se colocan parametros aplicables como la hora su estado etc..
    hour = models.TimeField()
    #el TimeField se usa para tomar o introducir una hora
    date = models.DateField()
    #el DateField para la fecha
    created_at = models.DateTimeField(auto_now_add=True)
    #aqui el auto_now_add sirve para que te permita agrega automaticamente la fecha actual y no es editable
    updated_at = models.DateTimeField(auto_now=True)
    activity_type = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=StatusType.choices,
        default=StatusType.PENDING) 
    #aqui es donde utilizamos lo antes creado como una opcion y por defecto se coloca el pendiente en el caso que no llenemos el area
    place = models.CharField(
        max_length=50,
        choices=PlaceType.choices,
        default=PlaceType.CDO)
    #Lo mismo pero en lugares

    def __str__(self):
        return f'{self.date} - {self.place}'