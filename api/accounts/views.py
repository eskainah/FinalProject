from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import login, logout, get_user_model,authenticate
from rest_framework.permissions import AllowAny
<<<<<<< HEAD
=======
from rest_framework.authtoken.models import Token  # Import Token model
>>>>>>> 1331b330c336ba9da9e3dbd22af8b51d51f448e9
from .serializers import UserSerializer, LoginSerializer, SubAccountSerializer
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = UserSerializer(data=request.data)

        # Check if the provided role is 'admin'
        if request.data.get('role') != User.ADMIN:
            return Response(
                {"error": "Only users with the 'admin' role can register."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='register-sub-account')
    def register_sub_account(self, request):
        # pass the request context to the serializer
        if request.user.role != User.ADMIN:
            return Response({"error": "Only admins can create sub-accounts."}, status=status.HTTP_403_FORBIDDEN)

        serializer = SubAccountSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": f"{user.role.capitalize()} created successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login_view(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']  # Access the user object directly
            
            login(request, user)  # Log the user in

            # Generate or retrieve the token
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "message": "Login successful",
                "username": user.username,
                "role": user.role,
                "token": token.key,  # Include the token in the response
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='logout')
    def logout_view(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='accounts')
    def get_all_accounts(self, request):
        # Only admin can retrieve their sub-accounts
        if request.user.role != User.ADMIN:
            return Response({"error": "Only admins can retrieve accounts."}, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.filter(school_admin=request.user)  # Filter by the school admin
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_account(self, request, pk=None):
        """
        Only admins can delete accounts.
        """
        if not request.user.is_authenticated or request.user.role != User.ADMIN:
            return Response({"error": "Only admins can delete accounts."}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({"message": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], url_path='retrieve')
    def retrieve_account(self, request, pk=None):
        """
        Retrieve account details for admins or the logged-in user.
        """
        try:
            user = User.objects.get(pk=pk)
            if request.user.role == User.ADMIN or request.user.pk == user.pk:
                serializer = UserSerializer(user)
                return Response(serializer.data)
            return Response({"error": "You do not have permission to view this account."}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch'], url_path='update')
    def update_user(self, request, pk=None):
        """
        Update user details if the logged-in user is the target user or an admin.
        """
        try:
            user = User.objects.get(pk=pk)
            if not request.user.is_authenticated or (request.user.role != User.ADMIN and request.user.pk != user.pk):
                return Response({"error": "You do not have permission to update this user."}, status=status.HTTP_403_FORBIDDEN)

            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
