from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import Group

from users.models import User
from .models import Patient
from doctors.models import Doctor
from assistants.models import Assistant
from treatments.models import Treatment


class PatientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    doctors = serializers.PrimaryKeyRelatedField(many=True, queryset=Doctor.objects.all(), required=False)
    assistants = serializers.PrimaryKeyRelatedField(many=True, queryset=Assistant.objects.all(), required=False)
    recommended_treatment = serializers.PrimaryKeyRelatedField(queryset=Treatment.objects.all(), allow_null=True,
                                                               required=False)
    applied_treatment = serializers.PrimaryKeyRelatedField(queryset=Treatment.objects.all(), allow_null=True,
                                                           required=False)

    class Meta:
        model = Patient
        fields = ['user', 'doctors', 'assistants', 'recommended_treatment', 'applied_treatment']


    def create(self, validated_data):
        user_id = validated_data.pop('user').pk
        user = User.objects.get(pk=user_id)

        if Patient.objects.filter(user=user).exists():
            raise ValidationError({"message": "User already assigned"})

        patient = Patient.objects.create(user=user)

        doctors = validated_data.pop('doctors', [])
        assistants = validated_data.pop('assistants', [])

        if doctors:
            patient.doctors.set(doctors)  # Set doctors
        if assistants:
            patient.assistants.set(assistants)  # Set assistants

        patient.recommended_treatment = validated_data.get('recommended_treatment', None)
        patient.applied_treatment = validated_data.get('applied_treatment', None)
        patient.save()

        patient_group, created = Group.objects.get_or_create(name='patient')
        user.groups.add(patient_group)

        return patient


    def delete(self, instance):
        user = instance.user
        patient_group = Group.objects.get(name='patient')
        if patient_group in user.groups.all():
            user.groups.remove(patient_group)
        instance.delete()


class UpdateAppliedTreatmentSerializer(serializers.ModelSerializer):
    applied_treatment = serializers.PrimaryKeyRelatedField(queryset=Treatment.objects.all())

    class Meta:
        model = Patient
        fields = ['applied_treatment']


class UpdateRecommendedTreatmentSerializer(serializers.ModelSerializer):
    recommended_treatment = serializers.PrimaryKeyRelatedField(queryset=Treatment.objects.all())

    class Meta:
        model = Patient
        fields = ['recommended_treatment']


class UpdateUpdateAssignedAssistantsSerializer(serializers.ModelSerializer):
    assistants = serializers.PrimaryKeyRelatedField(queryset=Assistant.objects.all(), many=True)

    class Meta:
        model = Patient
        fields = ['assistants']

