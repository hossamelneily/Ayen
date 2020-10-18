from django.contrib.auth.password_validation import CommonPasswordValidator
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_auth.serializers import LoginSerializer
from django.conf import settings

from account.models import Account

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        write_only_fields = ['password']

    def validate(self, data):
        # validate email
        if data['email'] and User.objects.filter(email=data['email'].lower()):
            raise serializers.ValidationError(_("The Email already Existed"))

        data['email'] = data['email'].lower()

        return data


class CustomLoginSerializer(LoginSerializer):
    username = None

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = None
        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

            # Authentication through username
            elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(email, password)
            # Authentication through either username or email
            else:
                user = self._validate_username_email(email, email, password)
        else:
            if email:
                try:
                    user_obj = User.objects.get(email__iexact=email)

                except User.DoesNotExist:
                    pass
                if user_obj:
                    user = self._validate_email(email, password)
        if user is None:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)
        attrs['user'] = user
        return attrs


class AccountMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('occupation',)


class UserSerializer(serializers.ModelField):
    class Meta:
        model = get_user_model()
        fields = ('email',)


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('occupation',)


class AccountDocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('passport_copy',)
