import logging
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    User = get_user_model()
    existing_user = User.objects.filter(username=username).first()

    logger.warning(
        "Login attempt: username=%s, user_exists=%s, is_active=%s, is_staff=%s, is_superuser=%s",
        username,
        existing_user is not None,
        getattr(existing_user, "is_active", None),
        getattr(existing_user, "is_staff", None),
        getattr(existing_user, "is_superuser", None),
    )

    user = authenticate(username=username, password=password)

    if user is not None:
        logger.warning("Login success: username=%s", username)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({'token': access_token, 'refresh': str(refresh)}, status=status.HTTP_200_OK)
    else:
        logger.warning("Login failed: username=%s", username)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not user.check_password(old_password):
        return Response({'message': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh_view(request):
    from rest_framework_simplejwt.views import TokenRefreshView
    return TokenRefreshView.as_view()(request)
