from rest_framework import serializers

from .models import User, Profile


class UserRegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=13)
    short_info = serializers.CharField()
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "password2", "profile_image", "phone_number", "short_info"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Неудачное подтверждение пароля!")

        if len(data["password"]) < 8:
            raise serializers.ValidationError("Пароль должен быть не менее 8 цифр!")

        if not data["password"].isdigit():
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну цифру!")

        if not data["password"].isupper():
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну заглавную букву!")

        if not data["password"].islower():
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну строчную букву!")

        if not "!@#%^$&*(){}[]?" in data["password"]:
            raise serializers.ValidationError("Пароль должен содержать хотя бы один спец.символ!")

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
        )
        profile_image = validated_data.get('profile_image')
        if profile_image:
            user.profile_image = profile_image
        user.set_password(validated_data["password"])
        user.save()
        try:
            profile = Profile.objects.create(
                user=user,
                phone_number=validated_data['phone_number'],
                short_info=validated_data['short_info']
            )
        except Exception as e:
            user.delete()
            raise e
        else:
            profile.username = user.username
            profile.profile_image = user.profile_image
        return profile
