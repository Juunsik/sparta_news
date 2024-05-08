from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]
        extra_kwargs = {
            "password": {"write_only": True}
        }  # 비밀번호 필드를 읽기 전용으로 설정

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # 비밀번호 해싱 자동 처리
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "date_joined",
            "description",
            "email",
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "description",
            "password",
            "password2",
<<<<<<< HEAD
        )
=======
        )
>>>>>>> 533891b914931f4f6b9035234547749b501e5e5f