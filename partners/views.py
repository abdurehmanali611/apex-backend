from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Partner
from .serializers import PartnerSerializer


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all().order_by("-id")
    serializer_class = PartnerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
