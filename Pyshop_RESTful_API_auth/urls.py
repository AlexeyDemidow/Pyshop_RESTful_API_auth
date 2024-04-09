from django.contrib import admin
from django.urls import path, include

from users.views import LoginView, RegisterView, RefreshView, LogoutView, ProfileView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Authentication API",
      default_version='v1',
      description="A simple RESTful API service for Authentication.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny, ],
)
#
#

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),

    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/refresh/', RefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),

    path('api/me/', ProfileView.as_view(), name='profile'),

    path('api/documentation/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/documentation/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/documentation/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

