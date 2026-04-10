from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'requests', views.RequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]