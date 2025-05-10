from django.urls import path, include
from rest_framework import routers

from authentication.views import SignupViewSet, LoginViewSet

router = routers.DefaultRouter()

router.register('signup', SignupViewSet, basename='signup')
router.register('login', LoginViewSet, basename='login')

urlpatterns = [
    path(r'auth/', include(router.urls)),
]