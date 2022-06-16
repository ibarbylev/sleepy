from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    lang = models.CharField(max_length=2, unique=True)

    def __str__(self) -> str:
        return f'{self.lang}'

    def save(self, *args, **kwargs):
        self.lang = self.lang.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        ordering = ['lang']


class UserProfile(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_MANAGER = 'manager'
    ROLE_CLIENT = 'client'
    ROLE_CONSULTANT = 'consultant'
    ROLE_CHOICES = [
        (ROLE_ADMIN, _("Admin")),
        (ROLE_MANAGER, _("Manager")),
        (ROLE_CLIENT, _("Client")),
        (ROLE_CONSULTANT, _("Consultant")),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default=ROLE_CLIENT)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    langs = models.ManyToManyField(Language, blank=True, verbose_name=_('languages'))
    date_of_birth = models.DateTimeField(null=True, blank=True, verbose_name=_('date of birth'))
    address = models.TextField(null=True, blank=True, verbose_name=_('address'))
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('phone number'))
    photo = models.ImageField(upload_to='images', null=True, blank=True, verbose_name=_('user photo'))
    note = models.TextField(null=True, blank=True)
    enable = models.BooleanField(null=True, blank=True)

    @property
    def is_superuser(self) -> bool:
        return self.role == self.ROLE_ADMIN

    @property
    def is_admin(self) -> bool:
        return self.role == self.ROLE_ADMIN

    @property
    def is_staff(self) -> bool:
        return self.role in [self.ROLE_ADMIN, self.ROLE_MANAGER]

    @property
    def is_client(self) -> bool:
        return self.role == self.ROLE_CLIENT

    @property
    def is_consultant(self) -> bool:
        return self.role == self.ROLE_MANAGER

    class Meta:
        verbose_name = _('UserProfile')
        verbose_name_plural = _('UserProfiles')
        ordering = ['-id']


