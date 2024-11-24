from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, UserListView, UserDetailView, ConfirmEmailView, \
    user_profile_edit
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('profile/edit/', user_profile_edit, name='user_profile_edit'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
