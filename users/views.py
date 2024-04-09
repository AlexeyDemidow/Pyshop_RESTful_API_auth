from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from .models import CustomUser, RefreshToken
from .serializers import UserSerializer, TokenObtainPairSerializer, TokenRefreshSerializer, TokenBlacklistSerializer, \
    ProfileSerializer


class CustomAutoSchema(SwaggerAutoSchema):

    def get_tags(self, operation_keys=None):
        tags = self.overrides.get('tags', None) or getattr(self.view, 'my_tags', [])
        if not tags:
            tags = [operation_keys[0]]

        return tags


class RegisterView(APIView):
    http_method_names = ['post']
    my_tags = ['Authentication']

    @swagger_auto_schema(
        operation_summary='User registration.',
        operation_description='Registering and creating a user profile.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'email', 'password']
        ),
        responses={
            HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        }
    )
    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            user = get_user_model().objects.create_user(**serializer.validated_data)
            return Response(status=HTTP_201_CREATED, data={'id': user.id, 'email': user.email})
        return Response(status=HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    my_tags = ['Authentication']
    @swagger_auto_schema(
        operation_summary='User login.',
        operation_description='Creating a token to log in to the user profile.',
        responses={
            HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super(LoginView, self).post(request, *args, **kwargs)


class RefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer
    my_tags = ['Authentication']

    @swagger_auto_schema(
        operation_summary='Refresh token.',
        operation_description='Refreshing a token to log in to the user profile.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
            return super(RefreshView, self).post(request, *args, **kwargs)


class LogoutView(TokenBlacklistView):
    serializer_class = TokenBlacklistSerializer
    my_tags = ['Authentication']

    @swagger_auto_schema(
        operation_summary='User logout.',
        operation_description='Logging out of the user profile and blacklisting a token.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super(LogoutView, self).post(request, *args, **kwargs)


class ProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProfileSerializer
    my_tags = ['Profile']

    def get_object(self):
        user = self.request.user.id
        querryset = CustomUser.objects.filter(id=user)
        me = get_object_or_404(querryset)
        return me

    @swagger_auto_schema(
        operation_summary='User info.',
        operation_description='Retrieving user profile information.'
    )
    def get(self, request, *args, **kwargs):
        return super(ProfileView, self).get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Profile update.',
        operation_description='Updating user data.'
    )
    def put(self, request, *args, **kwargs):
        return super(ProfileView, self).put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Partial profile update.',
        operation_description='Partial updating user data.'
    )
    def patch(self, request, *args, **kwargs):
        return super(ProfileView, self).patch(request, *args, **kwargs)

