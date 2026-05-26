from django.contrib.auth import get_user_model
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    # serializer que trabaja sobre el modelo User pero incluye campos del Profile anidado
    # source='profile.campo' permite acceder a campos del modelo Profile relacionado
    phone_number = serializers.CharField(source='profile.phone_number', required=False)
    # aqui se accede al telefono del perfil, no es obligatorio enviarlo
    image = serializers.ImageField(source='profile.image', required=False)
    # aqui se accede a la imagen del perfil, no es obligatoria
    group = serializers.SerializerMethodField(read_only=True)
    # SerializerMethodField permite calcular el valor del campo con un metodo personalizado
    # read_only=True significa que este campo nunca se puede enviar, solo se devuelve

    class Meta:
        model = get_user_model()
        # aqui se usa el modelo User de Django como base del serializer
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'image',
            'group',
            # group indica a que grupo pertenece el usuario (ej: "client", "admin")
        ]

        extra_kwargs = {
            'username': {'read_only': True},
            # el username no se puede cambiar desde este endpoint
            'email': {'read_only': True},
            # el email tampoco se puede cambiar desde aqui
        }

    @staticmethod
    def get_group(obj) -> str:
        # aqui se obtiene el nombre del primer grupo del usuario
        # si no tiene grupo asignado devuelve None
        return obj.groups.first().name if obj.groups.first() else None

    @staticmethod
    def update_profile(instance, data):
        # aqui se actualizan los campos del Profile relacionado al usuario
        phone_number = data.get('phone_number', None)
        if phone_number is not None:
            instance.profile.phone_number = phone_number
            # aqui se actualiza el telefono si se envio

        image = data.get('image', None)
        if image is not None:
            instance.profile.image = image
            # aqui se actualiza la imagen si se envio

        instance.profile.save()
        # aqui se guarda el perfil con los cambios realizados

    def update(self, instance, validated_data):
        # aqui se sobreescribe el metodo update para poder actualizar tambien el Profile
        profile = validated_data.pop('profile', {})
        # aqui se extrae la data del perfil del diccionario principal
        if bool(profile):
            self.update_profile(instance, profile)
            # si hay datos del perfil se actualiza el Profile

        return super().update(instance, validated_data)
        # aqui se actualiza el User con los datos restantes
