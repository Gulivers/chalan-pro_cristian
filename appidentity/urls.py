from rest_framework.routers import DefaultRouter
from .views import IdentityViewSet, UserViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'identity', IdentityViewSet, basename='identity')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
