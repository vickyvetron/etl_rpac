from django.contrib import admin
from .models import Company, Corporate, GlobalConfiguration
# Register your models here.

admin.site.register(Company)
admin.site.register(Corporate)
admin.site.register(GlobalConfiguration)