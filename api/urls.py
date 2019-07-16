from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'web_consult', views.WebConsultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]