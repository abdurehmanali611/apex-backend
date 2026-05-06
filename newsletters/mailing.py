import html
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection

from .models import NewsletterIssue

logger = logging.getLogger(__name__)


def _build_html_body(issue: NewsletterIssue) -> str:
    title = html.escape(issue.title)
    body = html.escape(issue.content).replace("\n", "<br>\n")
    site = html.escape(getattr(settings, "SITE_PUBLIC_URL", "https://www.apexsolutionhub.com"))
    return f"""<!DOCTYPE html>
<html><body style="font-family:system-ui,-apple-system,sans-serif;line-height:1.6;color:#111;background:#f6f6f6;padding:24px;">
<div style="max-width:560px;margin:0 auto;background:#fff;padding:28px;border-radius:12px;border:1px solid #e5e5e5;">
<p style="margin:0 0 16px;font-size:13px;color:#666;">Apex Solution — IT Insights</p>
<h1 style="margin:0 0 16px;font-size:22px;color:#111;">{title}</h1>
<div style="font-size:15px;color:#333;">{body}</div>
<hr style="margin:28px 0;border:none;border-top:1px solid #eee;" />
<p style="margin:0;font-size:12px;color:#888;">You subscribed at <a href="{site}" style="color:#2563eb;">{site}</a></p>
</div></body></html>"""


def send_newsletter_issue_email(issue: NewsletterIssue) -> dict:
    """
    Send one SMTP message per subscriber using a shared connection.
    Requires EMAIL_* settings (see BackEnd/.env.example).
    """
    if not getattr(settings, "NEWSLETTER_SEND_EMAILS", True):
        return {"skipped": True, "reason": "NEWSLETTER_SEND_EMAILS is False"}

    host = getattr(settings, "EMAIL_HOST", "") or ""
    if not host.strip():
        raise RuntimeError(
            "SMTP is not configured: set EMAIL_HOST (and related EMAIL_* variables) in BackEnd/.env. "
            "See BackEnd/.env.example."
        )

    recipients = list(
        issue.recipients.filter(is_active=True).values_list("email", flat=True)
    )
    if not recipients:
        return {"sent": 0, "total": 0, "message": "No active subscribers"}

    from_email = settings.DEFAULT_FROM_EMAIL
    subject = issue.subject
    text_body = f"{issue.title}\n\n{issue.content}"
    html_body = _build_html_body(issue)

    sent = 0
    errors: list[dict] = []

    connection = get_connection()
    connection.open()
    try:
        for to_addr in recipients:
            try:
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_body,
                    from_email=from_email,
                    to=[to_addr],
                    connection=connection,
                )
                msg.attach_alternative(html_body, "text/html")
                msg.send(fail_silently=False)
                sent += 1
            except Exception as exc:
                logger.exception("Newsletter SMTP failed for %s", to_addr)
                errors.append({"email": to_addr, "error": str(exc)})
    finally:
        connection.close()

    return {
        "sent": sent,
        "total": len(recipients),
        "failed": len(errors),
        "errors": errors[:20],
    }
