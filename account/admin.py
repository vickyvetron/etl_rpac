import site
from django.contrib import admin
from .models import CustomUser, Role, Otp

admin.site.register(CustomUser)
admin.site.register(Role)
admin.site.register(Otp)

