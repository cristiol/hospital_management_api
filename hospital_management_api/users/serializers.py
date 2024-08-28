from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'username', 'password']

    def create(self, validated_data):
        user = User(
            full_name=validated_data['full_name'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        for field in validated_data:
            if field != 'password':
                setattr(instance, field, validated_data[field])

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance