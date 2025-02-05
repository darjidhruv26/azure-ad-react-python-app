from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from authapp.authentication import AzureADAuthentication

class DashboardView(APIView):
    authentication_classes = [SessionAuthentication, AzureADAuthentication] 
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email if user.email else "Not Available",
            "full_name": user.first_name if user.first_name else "Not Available",
            "message": f"Welcome, {user.first_name}!"
        })

class UserLogout(APIView):
    def post(self, request):
        return Response({"message": "Logout Successful"})