from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet

router = DefaultRouter(trailing_slash=False)
router.register("", ServiceViewSet, basename="services")

urlpatterns = router.urls
