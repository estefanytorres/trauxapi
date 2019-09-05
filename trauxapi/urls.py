from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', include('api.urls')),
    path(r'api-token/auth/', TokenObtainPairView.as_view()),
    path(r'api-token/verify/', TokenVerifyView.as_view()),
    path(r'api-token/refresh/', TokenRefreshView.as_view()),
    # TODO: destroy token
    # path(r'api-token/destroy/', TokenRefreshView.as_view()),
]

