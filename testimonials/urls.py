from rest_framework.routers import DefaultRouter
from .views import TestimonialViewSet

router = DefaultRouter(trailing_slash=False)
router.register("", TestimonialViewSet, basename="testimonials")

urlpatterns = router.urls
