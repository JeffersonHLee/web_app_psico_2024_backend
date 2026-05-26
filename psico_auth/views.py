from django.conf import settings
from django.shortcuts import redirect

def password_reset_redirect(request, uidb64, token):
    # aqui se redirige al usuario al formulario de reset de contrasena en el frontend
    # uidb64 es el id del usuario codificado y token es el codigo de verificacion
    return redirect(f'{settings.FRONTEND_URL}/accounts/password/reset/confirm/{uidb64}/{token}')
