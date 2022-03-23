from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Поле phone не может быть пустым! ')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Администратор должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Администратор должен иметь is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=12, unique=True)
    invite_code = models.CharField(max_length=6, unique=True)
    confirm_code = models.CharField(blank=True, null=True, max_length=4)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone'

    objects = CustomUserManager()

    def __str__(self):
        return self.phone


class Invitation(models.Model):
    invitee = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='invitee',
        verbose_name='Приглашенный')
    inviter = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='inviter',
        verbose_name='Приглашающий')

    class Meta:
        verbose_name = 'Invite'
        verbose_name_plural = 'Invites'

    def __str__(self):
        return self.invitee.phone
