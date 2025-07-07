from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CrewViewSet, TruckViewSet, CategoryListView, SupervisorCommunitiesView

router = DefaultRouter()
router.register(r'crews', CrewViewSet)
router.register(r'trucks', TruckViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/categories/', CategoryListView.as_view(), name='category-list'),
    path('api/supervisor-communities/', SupervisorCommunitiesView.as_view(), name='supervisor-communities'),
]
