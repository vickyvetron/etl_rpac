from djongo import models
from django import forms
# Create your models here.

from django.db.models.signals import post_save
from django.dispatch import receiver

from account.utils import mail_send
from django.conf import settings


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_no = models.BigIntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=255)
    no_pods = models.BigIntegerField()
    dev_url = models.CharField(max_length=255)
    dev_user_id = models.CharField(max_length=55)
    dev_password = models.CharField(max_length=255)
    prod_url = models.CharField(max_length=255)
    prod_user_id = models.CharField(max_length=55)
    prod_password = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Corporate(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=55)
    email = models.EmailField()
    no_pods = models.BigIntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.brand


class GlobalConfiguration(models.Model):
    id = models.AutoField(primary_key=True)
    optional_fields = models.JSONField()
    required_fields = models.JSONField()
    corporate = models.OneToOneField(Corporate, on_delete=models.CASCADE)

    objects = models.DjongoManager()


    def __str__(self) -> str:
        return self.corporate.brand


class JobDetail(models.Model):
    id = models.AutoField(primary_key=True)
    comapany = models.ForeignKey(Company, on_delete=models.CASCADE)
    corporate = models.ForeignKey(Corporate, on_delete=models.CASCADE)
    job_id_no = models.CharField(max_length=255)
    job_name = models.CharField(max_length=55)
    file_mask = models.CharField(max_length=255)
    execution_schedule = models.DateTimeField()
    active_version_no = models.CharField(max_length=55)
    send_notification = models.BooleanField(default=False)
    path = models.CharField(max_length=255, null=True, blank=True)
    host = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.job_name} - {self.job_id_no}"


@receiver(post_save, sender=JobDetail, dispatch_uid="update_stock_count")
def update_stock(sender, instance, **kwargs):
    try:
        if instance.send_notification == True:
            email = instance.corporate.email
            mesg = f"Job Succesfully created with. Job Name {instance.job_name} Job ID No {instance.job_id_no}. Job Execution Time:- {instance.execution_schedule}"
            mail = mail_send("Job Created Succesfully", mesg, settings.EMAIL_HOST_USER, [email])
    except Exception as e:
        pass
