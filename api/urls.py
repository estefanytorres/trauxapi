from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()

router.register(r'user', views.UserViewSet)
router.register(r'web_consult', views.WebConsultViewSet)
router.register(r'client', views.ClientViewSet)
router.register(r'file_transaction', views.FileTransactionViewSet)
router.register(r'file', views.FileViewSet)

# router.register(r'toolbox/message/set', views.MessageSetViewSet)
# router.register(r'toolbox/message/catalog', views.MessageCatalogViewSet)

# router.register(r'sys/client', views.ClientViewSet)
# router.register(r'sys/module', views.ModuleViewSet)
# router.register(r'sys/license', views.LicenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
