from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path(r'api-token-auth/', obtain_jwt_token),
    path(r'api-token-refresh/', refresh_jwt_token),
]

