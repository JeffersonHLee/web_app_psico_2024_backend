from dj_rest_auth import views as dra_views
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView

from django.urls import path

from rest_framework_simplejwt.views import TokenVerifyView

from psico_auth.views import password_reset_redirect

urlpatterns = [
    path('login/', dra_views.LoginView.as_view()),
    # POST /api/v1/auth/login/ — inicia sesion y devuelve access_token y refresh_token

    path('registration/', RegisterView.as_view()),
    # POST /api/v1/auth/registration/ — registra un usuario nuevo con el UserRegisterSerializer

    path('token/verify/', TokenVerifyView.as_view()),
    # POST /api/v1/auth/token/verify/ — verifica si un token sigue siendo valido

    path('token/refresh/', get_refresh_view().as_view()),
    # POST /api/v1/auth/token/refresh/ — renueva el access_token usando el refresh_token

    path('password/reset/', dra_views.PasswordResetView.as_view()),
    # POST /api/v1/auth/password/reset/ — envia un email con el enlace para resetear contrasena

    path('password/reset/confirm/', dra_views.PasswordResetConfirmView.as_view()),
    # POST /api/v1/auth/password/reset/confirm/ — confirma el nuevo password con el codigo del email

    path('password/reset/redirect/<uidb64>/<token>/',
         password_reset_redirect,
         name='password_reset_confirm'),
    # GET — redirige al usuario al formulario de reset en el frontend
    # uidb64 es el id del usuario codificado y token es el codigo de verificacion
]
