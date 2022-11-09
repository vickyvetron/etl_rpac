from djongo import models
from django import forms
# Create your models here.


class Company(models.Model):
    id = models.BigIntegerField(primary_key=True)
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
    id = models.BigIntegerField(primary_key=True)
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