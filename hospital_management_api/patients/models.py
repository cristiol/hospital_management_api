from django.db import models
from doctors.models import Doctor
from assistants.models import Assistant
from treatments.models import Treatment
from users.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctors = models.ManyToManyField(Doctor, blank=True)
    assistants = models.ManyToManyField(Assistant, blank=True)
    recommended_treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, blank=True, null=True,
                                              related_name='recommended_treatment')
    applied_treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, blank=True, null=True,
                                          related_name='applied_treatment')

    def __str__(self):
        return F"Patient {self.user.full_name}"
