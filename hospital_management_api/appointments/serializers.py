from rest_framework import serializers
from .models import Slot, Appointment


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'slot', 'status']

    def validate(self, data):
        doctor_id = data['doctor'].id
        slot = data['slot']
        doctor_slots = Slot.objects.filter(doctor_id=doctor_id, is_booked=False)

        if slot not in doctor_slots:
            raise serializers.ValidationError(f"{data['doctor']} doesn't have this slot")

        if self.instance is None and data['slot'].is_booked:
            raise serializers.ValidationError("This time slot is already reserved.")

        if self.instance and data.get('slot') and data['slot'] != self.instance.slot and data['slot'].is_booked:
            raise serializers.ValidationError("The new time slot is already reserved.")

        return data

    def create(self, validated_data):
        appointment = Appointment.objects.create(**validated_data)
        slot = validated_data['slot']
        slot.is_booked = True
        slot.save()
        return appointment

    def update(self, instance, validated_data):
        if 'slot' in validated_data:
            old_slot = instance.slot
            new_slot = validated_data['slot']

            if old_slot != new_slot:
                old_slot.is_booked = False
                old_slot.save()

                new_slot.is_booked = True
                new_slot.save()

        return super().update(instance, validated_data)
