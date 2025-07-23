from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, AudioFragmentViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'fragments', AudioFragmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
