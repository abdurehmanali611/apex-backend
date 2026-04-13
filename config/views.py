from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from services.models import Service
from portfolio.models import Portfolio
from blogs.models import Blog
from teams.models import Team
from partners.models import Partner
from contacts.models import Contact
from testimonials.models import Testimonial
from django.utils import timezone
from datetime import timedelta

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    # Counts
    services_count = Service.objects.count()
    portfolios_count = Portfolio.objects.count()
    blogs_count = Blog.objects.count()
    teams_count = Team.objects.count()
    partners_count = Partner.objects.count()
    contacts_count = Contact.objects.count()
    testimonials_count = Testimonial.objects.count()

    # Recent activities (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_contacts = Contact.objects.filter(created_at__gte=week_ago).order_by('-created_at')[:5]
    recent_blogs = Blog.objects.filter(date__gte=week_ago.date()).order_by('-date')[:5]
    # For others, if no date field, just recent by id or something, but for now, use contacts and blogs

    data = {
        'counts': {
            'services': services_count,
            'portfolios': portfolios_count,
            'blogs': blogs_count,
            'teams': teams_count,
            'partners': partners_count,
            'contacts': contacts_count,
            'testimonials': testimonials_count,
        },
        'recent_activities': {
            'contacts': [
                {
                    'id': c.id,
                    'name': c.Full_Name,
                    'email': c.Email,
                    'subject': c.Subject,
                    'created_at': c.created_at,
                } for c in recent_contacts
            ],
            'blogs': [
                {
                    'id': b.id,
                    'title': b.title,
                    'date': b.date,
                } for b in recent_blogs
            ],
        }
    }
    return Response(data)