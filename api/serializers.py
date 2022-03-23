from rest_framework import serializers

from .models import CustomUser, Invitation
from .generators import confirm_code, invite_code


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('phone', 'confirm_code')
        read_only_fields = ('confirm_code',)
        model = CustomUser
        extra_kwargs = {'phone': {'validators': []}, }

    @staticmethod
    def unique_check(invitation_code):
        check = CustomUser.objects.filter(
                invite_code=invitation_code)
        while check.exists():
            invitation_code = invite_code()
        return invitation_code

    def create(self, validated_data):
        code = confirm_code()
        invitation_code = invite_code()
        code_checked = self.unique_check(invitation_code)
        user = CustomUser.objects.create(
                invite_code=code_checked,
                confirm_code=code, **validated_data)
        # отправка кода на телефон
        return user

    def validate(self, data):
        phone = data['phone']
        user = CustomUser.objects.filter(phone=phone)
        if user.exists():
            user_existing = CustomUser.objects.get(phone=phone)
            code = confirm_code()
            user_existing.confirm_code = code
            user_existing.save(update_fields=['confirm_code'])
            # отправка кода на телефон
            raise serializers.ValidationError(
                f'Вы уже зарегистрированы, ваш код - {code}')
        return data


class ProfileSerializer(serializers.ModelSerializer):
    invite = serializers.StringRelatedField(source='inviter', many=True)
    is_activated = serializers.SerializerMethodField()

    class Meta:
        fields = ('phone', 'invite_code', 'invite', 'is_activated')
        model = CustomUser

    def get_is_activated(self, obj):
        inviter = Invitation.objects.filter(invitee=obj)
        if inviter.exists():
            user = Invitation.objects.get(invitee=obj)
            return user.inviter.invite_code
        return None


class TokenSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=16)
    confirm_code = serializers.CharField(max_length=4)


class MyProfileSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)
    

