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
    following_user = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('following_user',)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following_user']
            )
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        following_user = validated_data['following_user']

        if user == following_user:
            raise serializers.ValidationError('자기 자신을 팔로우할 수 없습니다.')

        follow, created = Follow.objects.get_or_create(
            user=user,
            following_user=following_user
        )

        if not created:
            raise serializers.ValidationError('이미 팔로우한 사용자입니다.')

        return follow