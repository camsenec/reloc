from rest_framework import routers
from .views import EdgeServerViewSet, ClientViewSet, ClusterViewSet, AreaViewSet


router = routers.DefaultRouter()
router.register(r'^server', EdgeServerViewSet)
router.register(r'^user', ClientViewSet)
router.register(r'^cluster', ClusterViewSet)
router.register(r'^area', AreaViewSet)
