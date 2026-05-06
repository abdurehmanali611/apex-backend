from rest_framework import serializers
from .models import NewsletterIssue, NewsletterSubscriber


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = "__all__"
        read_only_fields = ("created_at",)


class NewsletterIssueSerializer(serializers.ModelSerializer):
    recipient_emails = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = NewsletterIssue
        fields = "__all__"
        read_only_fields = ("created_at", "recipients_count", "recipients", "recipient_emails")

    def get_recipient_emails(self, obj):
        return list(obj.recipients.values_list("email", flat=True))

    def create(self, validated_data):
        issue = NewsletterIssue.objects.create(**validated_data)
        active_subscribers = NewsletterSubscriber.objects.filter(is_active=True)
        issue.recipients.set(active_subscribers)
        issue.recipients_count = active_subscribers.count()
        issue.save(update_fields=["recipients_count"])
        return issue
