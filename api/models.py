from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    A custom User model based on AbstractUser class.
    """

    def __str__(self):
        return self.username


class Task(models.Model):
    """
    A custom Task model.
    """
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=('Name'),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=('Description'),
    )
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='creator',
        verbose_name=('Creator'),
    )
    executor = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='executor',
        verbose_name=('Executor'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name
