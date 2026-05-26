from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _

from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer

from profiles.models import Profile


class UserRegisterSerializer(RegisterSerializer):
    # serializer personalizado que extiende el registro base de dj-rest-auth
    # aqui se agregan campos extra que no vienen por defecto en el registro
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=25, write_only=True)
    # write_only=True significa que el telefono se recibe pero nunca se devuelve en la respuesta

    def validate_email(self, email: str):
        # aqui se valida que el email no este ya registrado en el sistema
        already_user = get_user_model().objects \
            .filter(email__exact=email.strip()) \
            .exists()

        if already_user:
            raise serializers.ValidationError(
                _('A user is already registered with this e-mail address.'))

        return super().validate_email(email)

    def get_cleaned_data(self):
        # aqui se agregan los campos extra al diccionario de datos validados
        return {
            **super().get_cleaned_data(),
            # ** extiende los datos ya validados por el RegisterSerializer base

            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }

    def save(self, request):
        # aqui se ejecuta todo al momento de registrar un usuario nuevo
        phone_number = self.validated_data.pop('phone_number')
        # aqui se saca el telefono de los datos validados para usarlo por separado

        group, _ = Group.objects.get_or_create(name='client')
        # aqui se obtiene o crea el grupo "client" para asignarselo al nuevo usuario

        user = super().save(request)
        # aqui se crea el usuario con los datos del RegisterSerializer base
        user.groups.add(group)
        # aqui se asigna el usuario al grupo "client"
        Profile.objects.create(
            user=user,
            phone_number=phone_number)
        # aqui se crea automaticamente el perfil del usuario con su numero de telefono

        return user

class UserSerializer(serializers.Serializer):
    # serializer de solo lectura para devolver los datos basicos de un usuario
    # se usa en AppointmentReadSerializer y ActivityReadSerializer para mostrar el doctor
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()