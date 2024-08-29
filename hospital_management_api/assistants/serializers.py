from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import Assistant, User
from rest_framework.exceptions import ValidationError


class AssistantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Assistant
        fields = '__all__'

    def create(self, validated_data):
        user_id = validated_data['user'].pk
        user = User.objects.get(pk=user_id)

        if Assistant.objects.filter(user=user).exists():
            raise ValidationError({"message": "User already assigned"})

        assistant = Assistant.objects.create(user=user)
        assistant_group, created = Group.objects.get_or_create(name='assistant')
        user.groups.add(assistant_group)

        return assistant


    def delete(self, instance):
        user = instance.user
        assistant_group = Group.objects.get(name='assistant')
        if assistant_group in user.groups.all():
            user.groups.remove(assistant_group)
        instance.delete()
