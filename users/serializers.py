from typing import Dict, Any
import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer as JwtTokenRefreshSerializer
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer as JwtTokenBlacklistSerializer
from rest_framework_simplejwt.settings import api_settings

from .models import RefreshToken
from Pyshop_RESTful_API_auth import settings


class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        data.clear()
        refresh = self.get_token(self.user)

        data["access_token"] = str(refresh.access_token)
        data["refresh_token"] = str(refresh)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        RefreshToken.objects.create(
            token=str(refresh),
            user=self.user,
            expire_time=datetime.datetime.today() + settings.SIMPLE_JWT.get("SLIDING_TOKEN_REFRESH_LIFETIME")
        )

        return data


class TokenRefreshSerializer(JwtTokenRefreshSerializer):
    refresh_token = serializers.CharField(required=False)
    refresh = refresh_token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        refresh_token = self.token_class(attrs["refresh"])
        data = {"access_token": str(refresh_token.access_token)}
        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh_token.blacklist()
                except AttributeError:
                    pass

            refresh_token.set_jti()
            refresh_token.set_exp()
            refresh_token.set_iat()

            data["refresh_token"] = str(refresh_token)

        return data


class TokenBlacklistSerializer(JwtTokenBlacklistSerializer):
    refresh_token = serializers.CharField(write_only=True)
    refresh = refresh_token

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        success = 'User logged out.'
        refresh = self.token_class(attrs["refresh"])
        try:
            refresh.blacklist()
            RefreshToken.objects.filter(token=refresh).delete()
        except AttributeError:
            pass
        return {'success': success}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email')
