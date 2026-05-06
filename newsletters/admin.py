from django.contrib import admin
from .models import NewsletterIssue, NewsletterSubscriber


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "created_at")
    search_fields = ("email",)
    list_filter = ("is_active",)


@admin.register(NewsletterIssue)
class NewsletterIssueAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "recipients_count", "created_at")
    search_fields = ("title", "subject", "content")
