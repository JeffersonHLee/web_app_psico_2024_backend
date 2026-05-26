from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class Patient(models.Model):

    class PlaceTypes(models.TextChoices):
        # aqui se crean las opciones del lugar de atencion del paciente
        CDO = 'CDO', _('CDO')
        SEMILLERO = 'SEMILLERO', _('Semillero')
        EXTERNAL = 'EXTERNAL', _('Externo')

    name = models.TextField()
    # nombre del paciente
    phone = models.CharField(max_length=25, blank=True, default='')
    # numero de telefono del paciente, no es obligatorio
    age = models.IntegerField()
    # edad del paciente
    place = models.CharField(
        max_length=50,
        choices=PlaceTypes.choices,
        default=PlaceTypes.CDO)
    # lugar donde se atiende el paciente, por defecto CDO
    pacientNumber = models.IntegerField(blank=True, default=0)
    # numero de expediente del paciente
    created_at = models.DateTimeField(auto_now_add=True)
    # fecha en que se registro el paciente, se agrega automaticamente
    grade = models.TextField(blank=True,default='')
    # grado escolar del paciente, no es obligatorio
    state = models.BooleanField()
    # indica si el paciente esta activo o no
    stateDescription = models.TextField(blank=True, default='')
    # descripcion del estado del paciente, no es obligatorio

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='patient'
        # PROTECT evita que se elimine un usuario si tiene pacientes registrados
    )

    def __str__(self):
        return f'{self.name} - {self.phone} - {self.age}'