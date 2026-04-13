from rest_framework.routers import DefaultRouter
from .views import ContactViewSet

router = DefaultRouter(trailing_slash=False)
router.register("", ContactViewSet, basename="contacts")

urlpatterns = router.urls
