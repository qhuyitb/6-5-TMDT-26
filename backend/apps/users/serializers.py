import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Email hoặc mật khẩu không chính xác.")

        if user.status == 'locked':
            raise serializers.ValidationError("Tài khoản của bạn đã bị khóa.")

        if user.status == 'inactive':
            raise serializers.ValidationError("Tài khoản chưa được kích hoạt.")

        data['user'] = user
        return data