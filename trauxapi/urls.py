# Django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# REST_framework
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


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)