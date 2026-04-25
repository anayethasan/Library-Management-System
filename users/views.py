from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class LogoutViewSet(APIView):
    """
    POST /api/auth/logout/
    Logs out the currently authenticated user by blacklisting their refresh token.
 
    Request body:
        { "refresh": "<refresh_token>" }
 
    Response (204):
        { "detail": "Successfully logged out." }
 
    Response (400):
        { "error": "<error_message>" }
 
    Note: Requires 'rest_framework_simplejwt.token_blacklist' in INSTALLED_APPS.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)