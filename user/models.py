from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import DateField, TextField, EmailField
import random


class CustomUserModel(AbstractUser):
    birth_date=DateField(blank=False, null=True)
    token=TextField(blank=False, null=True)
    confirm=models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.change_token()
        return super().save(*args, **kwargs)

    def change_token(self):
        self.token=''
        abc='ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
        for _ in range(random.randint(25,35)):
            self.token+=random.choice(abc)
        return self.token


    def __str__(self):
        return self.username