from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import HeroStat
from .serializers import HeroStatSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def hero_footer_list(request):
    queryset = HeroStat.objects.all().order_by("id")
    serializer = HeroStatSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def hero_footer_update(request, name):
    try:
        hero_stat = HeroStat.objects.get(name=name)
    except HeroStat.DoesNotExist:
        return Response(
            {"message": "Hero footer item not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = HeroStatSerializer(hero_stat, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
