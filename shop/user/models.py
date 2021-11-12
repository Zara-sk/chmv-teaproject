from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)

    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=15, verbose_name='Телефон')
    username = models.CharField(blank=True, null=True, max_length=255)

    REQUIRED_FIELDS = ['username']

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email