import logging
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import OperationalError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
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

        logger.warning("Login failed: username=%s", username)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except OperationalError:
        logger.exception("Login failed because the database connection is unavailable")
        return Response(
            {'message': 'Login is temporarily unavailable. Please try again shortly.'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    except Exception:
        logger.exception("Unexpected login error")
        return Response(
            {'message': 'Unable to process login right now.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


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
    serializer = TokenRefreshView.serializer_class(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except Exception as exc:
        logger.exception("Token refresh failed")
        raise exc
    return Response(serializer.validated_data, status=status.HTTP_200_OK)
