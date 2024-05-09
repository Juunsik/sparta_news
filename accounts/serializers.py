from rest_framework import serializers
from .models import User, Follow
from rest_framework.validators import UniqueTogetherValidator

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
        )


class FollowSerializer(serializers.ModelSerializer):
    followed = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('followed',)

    def validate_followed(self, value):
        user = self.context['request'].user
        if user == value:
            raise serializers.ValidationError("스스로를 팔로우할 순 없습니다.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        followed = validated_data['followed']
        follow, created = Follow.objects.get_or_create(follower=user, followed=followed)
        if not created:
            follow.delete()
        return follow