from rest_framework.routers import DefaultRouter
from .views import NewsletterIssueViewSet, NewsletterSubscriberViewSet

router = DefaultRouter(trailing_slash=False)
router.register("subscribers", NewsletterSubscriberViewSet, basename="newsletter-subscribers")
router.register("issues", NewsletterIssueViewSet, basename="newsletter-issues")

urlpatterns = router.urls
