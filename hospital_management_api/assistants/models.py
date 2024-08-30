from django.db import models
from users.models import User


class Assistant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def name(self):
        return self.user.full_name

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return f"Assistant {self.user.full_name}"