from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_STUDENT = 'student'
    ROLE_CHOICES = (
        (ROLE_ADMIN, 'Администратор'),
        (ROLE_STUDENT, 'Ученик'),
    )
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_BLOCKED = 'blocked'
    STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Активен'),
        (STATUS_INACTIVE, 'Неактивен'),
        (STATUS_BLOCKED, 'Заблокирован'),
    )

    username = None
    email = models.EmailField('Email', unique=True)
    name = models.CharField('Имя', max_length=120, blank=True)
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default=ROLE_STUDENT)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        ordering = ('-date_joined',)

    def __str__(self):
        return self.name or self.email

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN
