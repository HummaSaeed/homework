from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RequestOTPView, VerifyOTPView, LogoutView, ProfileView

app_name = 'accounts'

urlpatterns = [
    path('auth/request-otp/', RequestOTPView.as_view(), name='request_otp'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
