from rest_framework.routers import DefaultRouter
from .views import PartnerViewSet

router = DefaultRouter(trailing_slash=False)
router.register("", PartnerViewSet, basename="partners")

urlpatterns = router.urls
