from rest_framework.routers import DefaultRouter
from .views import PortfolioViewSet

router = DefaultRouter(trailing_slash=False)
router.register("", PortfolioViewSet, basename="portfolio")

urlpatterns = router.urls
