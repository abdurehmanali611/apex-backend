from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Contact
from .serializers import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by("-created_at", "-id")
    serializer_class = ContactSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
