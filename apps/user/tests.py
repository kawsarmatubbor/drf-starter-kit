from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.user.models import User, Verification


class UserApiTests(APITestCase):
    def test_signin_reports_unverified_email_when_password_is_correct(self):
        User.objects.create_user(
            email="unverified@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("signin"),
            {
                "email": "unverified@example.com",
                "password": "StrongPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["errors"]["non_field_errors"],
            ["Your email is not verified."],
        )

    def test_account_activation_otp_marks_email_verified(self):
        user = User.objects.create_user(
            email="activate@example.com",
            password="StrongPass123!",
        )
        Verification.objects.create(
            user=user,
            otp="123456",
            purpose="account_activation",
        )

        response = self.client.post(
            reverse("otp_verify"),
            {
                "email": "activate@example.com",
                "otp": "123456",
                "purpose": "account_activation",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_email_verified)
