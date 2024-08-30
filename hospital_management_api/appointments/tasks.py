from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import generate_slots
from appointments.models import Doctor, Patient, Slot


def send_newsletter_mail(email, appointment):
    template = 'email.html'

    context = {
        'email': email,
        'appointment': appointment
    }

    subject = 'Appointment confirmation'
    message = render_to_string(template, context)
    email_from = 'django_server007@outlook.com'
    recipient_list = [email, ]
    send_mail(
        subject=subject,
        message="",
        from_email=email_from,
        recipient_list=recipient_list,
        html_message=message,
    )


@shared_task
def send_confirmation_mail(data):
    doctor_id = data['doctor']
    doctor = Doctor.objects.get(pk=doctor_id)

    patient_id = data['patient']
    patient = Patient.objects.get(pk=patient_id)

    slot_id = data['slot']
    slot = Slot.objects.get(pk=slot_id)
    slot = slot.__str__()

    send_newsletter_mail(doctor.email, slot)
    send_newsletter_mail(patient.email, slot)


@shared_task
def periodic_tst():
    doctors = list(Doctor.objects.all())
    for doctor in doctors:
        generate_slots(doctor.id)

