from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(EmailGroup)
admin.site.register(EmailMessage)
admin.site.register(EmailSettings)