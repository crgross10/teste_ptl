from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core import validators
from django.utils.translation import ugettext_lazy as _
import re
from django.utils import timezone
import datetime


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('O nome do usuário deve ser informado'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user=self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user



class Usuario(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_('username'), max_length=15, unique=True, help_text=_('Required. 15 characters or fewer. Letters, numbers and @/./+/-/_ characters'), validators=[ validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), _('invalid'))])
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    cpf= models.CharField(max_length=11,null=False,blank=False)
    pis= models.CharField(max_length=11,null=False,blank=False)
    cep = models.CharField(max_length=150,null=False,blank=False)
    rua = models.CharField(max_length=150,null=False,blank=False)
    numero = models.CharField(max_length=20,null=False,blank=False)
    complemento = models.CharField(max_length=150,null=False,blank=False)
    municipio = models.CharField(max_length=150,null=False,blank=False)
    estado = models.CharField(max_length=2,null=False,blank=False)
    pais = models.CharField(max_length=50,null=False,blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def authenticate(username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(cpf=username)
            except  UserModel.DoesNotExist:
                try:
                    user = UserModel.objects.get(pis=username)
                except  UserModel.DoesNotExist:
                    return None
                else:
                    if user.check_password(password):
                        return user
                return None
            else:
                if user.check_password(password):
                    return user
            return None
        else:
            if user.check_password(password):
                return user
        return None


    def __str__(self):
       return  self.first_name

    objects = UserManager()
