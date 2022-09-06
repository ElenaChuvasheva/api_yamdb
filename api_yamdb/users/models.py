from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель User."""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        verbose_name='Nickname пользователя'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name='Фамилия пользователя'
    )
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLES,
        default=USER
    )
