from django.contrib import admin
from .models import Company, Corporate, GlobalConfiguration, JobDetail
# Register your models here.

admin.site.register(Company)
admin.site.register(Corporate)
admin.site.register(GlobalConfiguration)
admin.site.register(JobDetail)