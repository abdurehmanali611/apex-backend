from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Testimonial
from .serializers import TestimonialSerializer


class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all().order_by("-id")
    serializer_class = TestimonialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
