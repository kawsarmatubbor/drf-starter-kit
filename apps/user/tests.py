from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

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

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.activation_user.is_active)
        self.assertFalse(
            Verification.objects.filter(pk=self.activation_verification.pk).exists()
        )

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


class OtpResendViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("otp_resend")
        self.inactive_user = User.objects.create_user(
            email="inactive@example.com",
            password="StrongPass123!",
        )
        self.active_user = User.objects.create_user(
            email="active@example.com",
            password="StrongPass123!",
            is_active=True,
        )

    @patch("apps.user.serializers.send_signup_otp_email")
    def test_resend_account_activation_otp_creates_new_verification(self, mocked_send_email):
        old_verification = Verification.objects.create(
            user=self.inactive_user,
            otp="111111",
            purpose="account_activation",
        )
        Verification.objects.filter(pk=old_verification.pk).update(
            created_at=timezone.now() - timedelta(minutes=6)
        )

        response = self.client.post(
            self.url,
            {
                "email": self.inactive_user.email,
                "purpose": "account_activation",
            },
            format="json",
        )

        verifications = Verification.objects.filter(
            user=self.inactive_user,
            purpose="account_activation",
            is_verified=False,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(verifications.count(), 1)
        self.assertNotEqual(verifications.first().otp, "111111")
        mocked_send_email.assert_called_once()

    @patch("apps.user.serializers.send_signup_otp_email")
    def test_resend_otp_rejects_request_within_cooldown(self, mocked_send_email):
        Verification.objects.create(
            user=self.inactive_user,
            otp="222222",
            purpose="account_activation",
        )

        response = self.client.post(
            self.url,
            {
                "email": self.inactive_user.email,
                "purpose": "account_activation",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            Verification.objects.filter(
                user=self.inactive_user,
                purpose="account_activation",
                is_verified=False,
            ).count(),
            1,
        )
        mocked_send_email.assert_not_called()

    @patch("apps.user.serializers.send_password_reset_otp_email")
    def test_resend_password_reset_otp_sends_reset_code(self, mocked_send_email):
        response = self.client.post(
            self.url,
            {
                "email": self.active_user.email,
                "purpose": "password_reset",
            },
            format="json",
        )

        verification = Verification.objects.filter(
            user=self.active_user,
            purpose="password_reset",
            is_verified=False,
        ).last()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(verification)
        mocked_send_email.assert_called_once()

    def test_resend_account_activation_rejects_active_user(self):
        response = self.client.post(
            self.url,
            {
                "email": self.active_user.email,
                "purpose": "account_activation",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
