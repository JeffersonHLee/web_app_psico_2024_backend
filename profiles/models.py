from django.db import models
from django.contrib.auth import get_user_model

def create_profile_image_path(instance, filename: str):
    # aqui se genera la ruta donde se guardara la imagen del perfil
    filename = filename.lower().replace(' ', '_').replace('-', '_')
    # aqui se convierte el nombre del archivo a minusculas y se reemplazan espacios y guiones por guion bajo

    return f'profiles/{instance.user.username}/{filename}'
    # la imagen se guarda en una carpeta con el nombre de usuario


class Profile(models.Model):
    # modelo que representa el perfil de un usuario del sistema
    user = models.OneToOneField(
        get_user_model(),
        related_name='profile',
        on_delete=models.CASCADE)
    # relacion uno a uno con el usuario, si se elimina el usuario se elimina el perfil

    completed = models.BooleanField(default=False)
    # indica si el usuario completo su perfil, por defecto es False

    image = models.ImageField(upload_to=create_profile_image_path, blank=True)
    # foto de perfil del usuario, no es obligatoria
    phone_number = models.CharField(max_length=25, blank=True, default='')
    # numero de telefono del usuario, no es obligatorio

    def __str__(self) -> str:
        return f"{self.user.username}'s Profile"
