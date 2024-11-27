from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар', null=True, blank=True, help_text='Загрузите свой аватар')
    phone_number = models.CharField(max_length=35, verbose_name='Телефон', blank=True, null=True, help_text='Введите номер телефона')
    country = models.CharField(max_length=100, verbose_name='Страна', blank=True, null=True, help_text='Напишите свою страну')

    token = models.CharField(max_length=100, verbose_name='Token',  blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Польлзователь'
        verbose_name_plural = 'Польлзователи'

    def __str__(self):
        return self.email
