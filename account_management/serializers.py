from rest_framework import serializers
from .models import Account
from django.contrib.auth.hashers import make_password


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'email', 'password', 'phone_number')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(RegistrationSerializer, self).create(validated_data)


class AccountPropertiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['pk', 'avatar', 'email', 'is_staff', 'is_active', 'bio', 'phone_number']


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['pk', 'avatar']
        readonly_fields = ['pk']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
