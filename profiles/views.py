from django.contrib.auth import get_user_model
from rest_framework.generics import  RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from profiles.serializers import ProfileSerializer


class UserProfile(RetrieveUpdateAPIView):
    # Vista para obtener y actualizar el perfil del usuario autenticado
    queryset = get_user_model().objects.all()
    # aqui trae todos los usuarios para buscar el que corresponde
    serializer_class = ProfileSerializer
    # aqui se convierte la informacion del perfil a Json
    permission_classes = [IsAuthenticated]
    # aqui se autentica para que solo usuarios registrados puedan acceder

    def get_object(self):
        # aqui se sobreescribe el metodo para devolver siempre el usuario que esta haciendo la peticion
        return self.request.user

class UserProfileList(ListAPIView):
    # Vista para listar todos los perfiles de usuarios
    queryset = get_user_model().objects.all()
    # aqui trae todos los usuarios registrados
    serializer_class = ProfileSerializer
    # aqui se convierte la informacion de los perfiles a Json
    permission_classes = [IsAuthenticated]
    # aqui se autentica para que solo usuarios registrados puedan acceder