from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Portfolio
from .serializers import PortfolioSerializer


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all().order_by("-id")
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
