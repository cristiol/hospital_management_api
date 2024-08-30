from datetime import datetime, timedelta, time
from django.db import models
from doctors.models import Doctor
from patients.models import Patient


class Slot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return (f"Slot for {self.doctor} -- {self.start_time.strftime('%Y-%m-%d')} --- {self.start_time.strftime('%H:%M')} - "
                f"{self.end_time.strftime('%H:%M')}")


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')

    slot = models.OneToOneField(Slot, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')

    def __str__(self):
        return f"Appointment {self.id}: {self.patient} with {self.doctor} at {self.slot.start_time}"



def generate_slots(doctor_pk):

    doctor = Doctor.objects.get(pk=doctor_pk)

    today = datetime.now().date()
    next_monday = today + timedelta(days=(7 - today.weekday()))

    for day in range(5):
        date = next_monday + timedelta(days=day)
        start_time = datetime.combine(date, time(12, 0))
        end_time = datetime.combine(date, time(17, 0))

        while start_time < end_time:
            Slot.objects.create(doctor=doctor, start_time=start_time, end_time=start_time + timedelta(hours=1))
            start_time += timedelta(hours=1)



