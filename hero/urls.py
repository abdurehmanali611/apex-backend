from django.urls import path
from .views import hero_footer_list, hero_footer_update

urlpatterns = [
    path("", hero_footer_list, name="hero-footer-list"),
    path("<str:name>", hero_footer_update, name="hero-footer-update"),
]
