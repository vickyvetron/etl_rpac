from email.policy import default
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.base_user import BaseUserManager


from django.db import models

class Role(models.Model):
    """
    Role models
    """
    name = models.CharField(unique=True, max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self._create_user(email, password, **extra_fields)

        admin_role, _ = Role.objects.get_or_create(name='admin')

        user.role.add(admin_role)
        user.save()

        return user



class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model
    """
    email = models.EmailField(unique=True)
    user_id = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.ManyToManyField(Role)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



class Otp(models.Model):
    TYPE = (
        ('Forgate_Password', 'Forgate_Password'),
        ('Chnage_password', 'Chnage_password')
    )
    id = models.BigIntegerField(primary_key=True)
    otp = models.CharField(max_length=55)
    type = models.CharField(choices=TYPE, max_length=55)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)