from django.urls import path
from profiles.views import UserProfile, UserProfileList

urlpatterns = [
    path('profile/', UserProfile.as_view(), name='user-profile'),
    # GET/PATCH /api/v1/profile/profile/ — ver o actualizar el perfil del usuario autenticado

    path('list/', UserProfileList.as_view(), name='user-profile-list'),
    # GET /api/v1/profile/list/ — listar todos los perfiles de usuarios registrados
]