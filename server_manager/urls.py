from rest_framework import routers
from .views import EdgeServerViewSet, ClientViewSet


router = routers.DefaultRouter()
router.register(r'^server', EdgeServerViewSet)
router.register(r'^user', ClientViewSet)
