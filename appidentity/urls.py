from rest_framework.routers import DefaultRouter
from .views import IdentityViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'identity', IdentityViewSet, basename='identity')

urlpatterns = [
    path('api/', include(router.urls)),
]
