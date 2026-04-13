from rest_framework.routers import DefaultRouter
from .views import BlogViewSet

router = DefaultRouter(trailing_slash=False)
router.register("", BlogViewSet, basename="blogs")

urlpatterns = router.urls
