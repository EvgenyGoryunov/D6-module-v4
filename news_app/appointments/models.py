from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Это модель записи на приём к кому угодно. Давайте будем думать, что это запись на приём к врачу. Здесь
# есть сообщение от пользователя, его имя и дата записи

class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'


class Appoint(models.Model):
    idpk = models.IntegerField()
    # idpkid = models.CharField(max_length=100, null=True)

    idpkid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.idpk}'
