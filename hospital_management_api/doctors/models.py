from django.db import models
from users.models import User


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def name(self):
        return self.user.full_name

    def __str__(self):
        return f"Doctor {self.user.full_name}"
