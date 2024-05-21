from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


def upload_to(instance, filename):
    return f'users/{instance.username}/{filename}'


class Profile(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, validators=[EmailValidator()])
    picture = models.ImageField(upload_to=upload_to, default='users/default/img.png')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='URL')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.username
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
