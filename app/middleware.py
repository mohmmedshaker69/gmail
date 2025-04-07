# middleware.py
from django.conf import settings
from .models import EmailSettings

class DynamicEmailSettingsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        email_settings = EmailSettings.objects.first()

        if email_settings:
            settings.EMAIL_HOST = email_settings.email_host
            settings.EMAIL_PORT = email_settings.email_port
            settings.EMAIL_USE_TLS = email_settings.email_use_tls
            settings.EMAIL_HOST_USER = email_settings.email_host_user
            settings.EMAIL_HOST_PASSWORD = email_settings.email_host_password
            settings.DEFAULT_FROM_EMAIL = email_settings.default_from_email
        else:

            settings.EMAIL_HOST = 'smtp.gmail.com'
            settings.EMAIL_PORT = 587
            settings.EMAIL_USE_TLS = True
            settings.EMAIL_HOST_USER = 'mohmmedshaker69@gmail.com'
            settings.EMAIL_HOST_PASSWORD = 'qwjs resc ecdg bcxu'
            settings.DEFAULT_FROM_EMAIL = settings.EMAIL_HOST_USER

        response = self.get_response(request)
        return response