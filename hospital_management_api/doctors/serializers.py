from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import Doctor, User
from rest_framework.exceptions import ValidationError


class DoctorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Doctor
        fields = '__all__'

    def create(self, validated_data):
        user_id = validated_data['user'].pk
        user = User.objects.get(pk=user_id)

        if Doctor.objects.filter(user=user).exists():
            raise ValidationError({"message": "User already assigned"})

        doctor = Doctor.objects.create(user=user)
        doctor_group, created = Group.objects.get_or_create(name='doctor')
        user.groups.add(doctor_group)

        return doctor


    def delete(self, instance):
        user = instance.user
        doctor_group = Group.objects.get(name='doctor')
        if doctor_group in user.groups.all():
            user.groups.remove(doctor_group)
        instance.delete()
