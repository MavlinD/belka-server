from django.contrib.auth.models import User
from django.db import models

from src.django_space.indicators.config import config


class Indicator(models.Model):
    """модель показателя"""

    name = models.CharField(max_length=config.IND_NAME_MAX_LENGTH)
    unit = models.CharField(max_length=config.IND_UNIT_MAX_LENGTH)
    desc = models.CharField(max_length=config.IND_DESC_MAX_LENGTH)

    def __str__(self):
        return self.name


class Log(models.Model):
    """модель сущности лога, связь один ко многим с показателем и пользователем."""

    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    ind_id = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    val = models.FloatField()
    date = models.DateTimeField()
