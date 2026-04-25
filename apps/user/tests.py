from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User, Verification


class OtpVerifyViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("otp_verify")
        self.activation_user = User.objects.create_user(
            email="otp@example.com",
            password="StrongPass123!",
        )
        self.activation_verification = Verification.objects.create(
            user=self.activation_user,
            otp="123456",
            purpose="account_activation",
        )
        self.reset_user = User.objects.create_user(
            email="reset@example.com",
            password="StrongPass123!",
            is_active=True,
        )
        self.reset_verification = Verification.objects.create(
            user=self.reset_user,
            otp="654321",
            purpose="password_reset",
        )

    def test_verify_account_activation_otp_activates_user(self):
        response = self.client.post(
            self.url,
            {
                "email": self.activation_user.email,
                "otp": self.activation_verification.otp,
                "purpose": "account_activation",
            },
            format="json",
        )

        self.activation_user.refresh_from_db()
        self.activation_verification.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.activation_user.is_active)
        self.assertTrue(self.activation_verification.is_verified)

    def test_verify_otp_rejects_invalid_otp(self):
        response = self.client.post(
            self.url,
            {
                "email": self.activation_user.email,
                "otp": "999999",
                "purpose": "account_activation",
            },
            format="json",
        )

        self.activation_user.refresh_from_db()
        self.activation_verification.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.activation_user.is_active)
        self.assertFalse(self.activation_verification.is_verified)
        self.assertIn("otp", response.data["errors"])

    def test_verify_otp_rejects_expired_otp(self):
        Verification.objects.filter(pk=self.activation_verification.pk).update(
            created_at=timezone.now() - timedelta(minutes=6)
        )

        response = self.client.post(
            self.url,
            {
                "email": self.activation_user.email,
                "otp": self.activation_verification.otp,
                "purpose": "account_activation",
            },
            format="json",
        )

        self.activation_user.refresh_from_db()
        self.activation_verification.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.activation_user.is_active)
        self.assertFalse(self.activation_verification.is_verified)

    def test_verify_password_reset_otp_marks_only_verification(self):
        response = self.client.post(
            self.url,
            {
                "email": self.reset_user.email,
                "otp": self.reset_verification.otp,
                "purpose": "password_reset",
            },
            format="json",
        )

        self.reset_user.refresh_from_db()
        self.reset_verification.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.reset_user.is_active)
        self.assertTrue(self.reset_verification.is_verified)
