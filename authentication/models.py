from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    lang = models.CharField(max_length=2, unique=True)


class User(AbstractBaseUser):
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    FIELDS_REQUIRED_FOR_CHECKOUT = [
        'username',
        'email',
        # 'first_name',
        # 'patronymic',
        # 'surname',
    ]

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

    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=64, choices=ROLE_CHOICES, default=ROLE_CLIENT)
    is_confirmed = models.BooleanField(default=False, verbose_name=_('is confirmed'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    langs = models.ManyToManyField(Language, blank=True, verbose_name=_('languages'))

    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('first name'))
    patronymic = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('patronymic'))
    surname = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('surname'))
    date_of_birth = models.DateTimeField(null=True, blank=True, verbose_name=_('date of birth'))
    address = models.TextField(null=True, blank=True, verbose_name=_('address'))
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('phone number'))
    photo = models.ImageField(upload_to='images', null=True, blank=True, verbose_name=_('user photo'))
    note = models.TextField(null=True, blank=True)
    enable = models.BooleanField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.surname}'

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
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-id']


