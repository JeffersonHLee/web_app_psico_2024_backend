from rest_framework import serializers
from patient.models import Patient

class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(
        # HiddenField significa que este campo no se pide al frontend ni aparece en la respuesta
        # CurrentUserDefault lo llena automaticamente con el usuario que esta haciendo la peticion
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Patient
        fields = '__all__'
        # fields = '__all__' incluye todos los campos del modelo Patient en el Json