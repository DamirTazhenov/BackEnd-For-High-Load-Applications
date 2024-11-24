from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import login_required


from .forms import UserProfileForm
from .models import EmailConfirmation, UserProfile
from .serializers import RegisterSerializer, TokenSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .throttles import CustomRoleBasedThrottle

import logging
logger = logging.getLogger('django.security')


# Registration API View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


# Custom Token Obtain Pair View to return more user data with the token
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            response.data.update({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
        return response


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ConfirmEmailView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [CustomRoleBasedThrottle]

    def post(self, request):
        code = request.data.get("confirmation_code")
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
            email_confirmation = user.email_confirmation

            if email_confirmation.confirmation_code != code:
                return Response({"error": "Invalid confirmation code."}, status=status.HTTP_400_BAD_REQUEST)

            if email_confirmation.is_confirmed:
                return Response({"message": "Email already confirmed."}, status=status.HTTP_400_BAD_REQUEST)

            if email_confirmation.is_expired():
                return Response({"error": "Confirmation code has expired."}, status=status.HTTP_400_BAD_REQUEST)

            email_confirmation.is_confirmed = True
            email_confirmation.save()
            return Response({"message": "Email confirmed successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except EmailConfirmation.DoesNotExist:
            return Response({"error": "Confirmation not found."}, status=status.HTTP_404_NOT_FOUND)

@login_required
def user_profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            logger.warning(f"Profile updated by user {request.user.username}: {profile}")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'user_profile_edit.html', {'form': form})