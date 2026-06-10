import random
from datetime import timedelta, datetime

from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, PhoneOTP
from .serializers import UserSerializer


def _generate_otp():
    return f"{random.randint(100000, 999999)}"


class RequestOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone = request.data.get('phone_number')
        if not phone:
            return Response({'success': False, 'message': 'phone_number is required'}, status=400)

        code = _generate_otp()
        now = timezone.now()
        expires = now + timedelta(minutes=5)

        otp = PhoneOTP.objects.create(phone_number=phone, code=code, expires_at=expires)

        # TODO: integrate SMS gateway to actually send the OTP to `phone`.

        return Response({'success': True, 'message': 'OTP generated', 'data': {'phone_number': phone, 'expires_at': expires}}, status=201)


class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('code')
        role = request.data.get('role', 'student')

        if not phone or not code:
            return Response({'success': False, 'message': 'phone_number and code are required'}, status=400)

        # find matching OTP
        now = timezone.now()
        otp_qs = PhoneOTP.objects.filter(phone_number=phone, code=code, is_used=False, expires_at__gte=now).order_by('-created_at')
        if not otp_qs.exists():
            return Response({'success': False, 'message': 'Invalid or expired OTP'}, status=400)

        otp = otp_qs.first()
        otp.is_used = True
        otp.save()

        user, created = User.objects.get_or_create(phone_number=phone, defaults={'username': phone, 'role': role})
        if created:
            user.set_unusable_password()
            user.save()

        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response({'success': True, 'message': 'Login successful', 'data': data})


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'success': False, 'message': 'refresh token required'}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'success': True, 'message': 'Logged out successfully'})
        except Exception:
            return Response({'success': False, 'message': 'Invalid token'}, status=400)


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
