from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .mailing import send_newsletter_issue_email
from .models import NewsletterIssue, NewsletterSubscriber
from .serializers import NewsletterIssueSerializer, NewsletterSubscriberSerializer


class NewsletterSubscriberViewSet(viewsets.ModelViewSet):
    queryset = NewsletterSubscriber.objects.all().order_by("-created_at", "-id")
    serializer_class = NewsletterSubscriberSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class NewsletterIssueViewSet(viewsets.ModelViewSet):
    queryset = NewsletterIssue.objects.all().order_by("-created_at", "-id")
    serializer_class = NewsletterIssueSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = dict(serializer.data)
        try:
            data["email_delivery"] = send_newsletter_issue_email(serializer.instance)
        except Exception as exc:
            data["email_delivery"] = {"success": False, "error": str(exc)}
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
