from rest_framework import serializers
from ..models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        user_permissions = validated_data.pop('user_permissions', [])
        user = CustomUser.objects.create_user(**validated_data)
        user.groups.set(groups)  # Assign groups after the user is created
        user.user_permissions.set(user_permissions)  # Assign user_permissions after the user is created
        return user

    def validate(self, data):
        if data.get('is_player') and not data.get('user_team') or data.get('user_height') or data.get('user_age'):
            raise serializers.ValidationError("Players must belong to a team, provide their height and age.")
        return data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
