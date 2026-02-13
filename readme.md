# DRF STARTER KIT

## Project Overview

This is a **Django REST Framework (DRF) authentication system** with:

- Email-based login (no username required)
- Account verification via OTP sent by email
- JWT authentication (access + refresh tokens) using Simple JWT
- User profile management (bio, gender, address, phone, avatar)
- Forgot password flow with OTP verification
- Resend OTP functionality for account verification and password reset

---

## Features

1. **User Registration**
    - Register with email and password.
    - OTP is sent via email to verify the account.
    - Account remains inactive until verified.

2. **Account Verification**
    - Verify account using OTP.
    - Resend OTP if needed.

3. **Login**
    - JWT-based login for verified users.
    - Refresh token support.

4. **Profile**
    - View and update profile information.
    - Fields include bio, gender, address, phone number, and avatar.

5. **Forgot Password**
    - Request password reset OTP.
    - Verify OTP and set a new password.
    - Resend OTP if needed.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/django-otp-auth.git
cd django-otp-auth
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `.env`

Create a `.env` file in the project root with the following:

```dotenv
# Database
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=5432

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Django secret
SECRET_KEY=your-secret-key
```

---

## Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Run the Server

```bash
python manage.py runserver
```

API will be available at `http://127.0.0.1:8000/`

---

## API Endpoints

| Endpoint                            | Method | Description                                                        |
| ----------------------------------- | ------ | ------------------------------------------------------------------ |
| `/register/`                        | POST   | Register new user (`email`, `password`, `password_2`)              |
| `/account-verification/`            | POST   | Verify account using OTP (`email`, `otp`)                          |
| `/resend-account-verification-otp/` | POST   | Resend account verification OTP (`email`)                          |
| `/login/`                           | POST   | JWT login (`email`, `password`)                                    |
| `/refresh/`                         | POST   | Refresh JWT token (`refresh`)                                      |
| `/profile/`                         | GET    | Get current user profile (JWT required)                            |
| `/profile/`                         | PUT    | Update profile (JWT required)                                      |
| `/forgot-password/`                 | POST   | Request password reset OTP (`email`)                               |
| `/forgot-password-verification/`    | POST   | Verify forgot password OTP (`email`, `otp`)                        |
| `/resend-forgot-password-otp/`      | POST   | Resend forgot password OTP (`email`)                               |
| `/set-new-password/`                | POST   | Set new password (`email`, `new_password`, `confirm_new_password`) |

---

## Usage Example

### Register

```bash
POST /register/
{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "Password123!",
  "password_2": "Password123!"
}
```

- OTP is sent to the user's email.

### Verify OTP

```bash
POST /account-verification/
{
  "email": "user@example.com",
  "otp": "123456"
}
```

- Activates the user account.

### Login

```bash
POST /login/
{
  "email": "user@example.com",
  "password": "Password123!"
}
```

- Returns JWT `access` and `refresh` tokens.

---

### Profile

**Get Profile**

```http
GET /profile/
Authorization: Bearer <access_token>
```

**Update Profile**

```http
PUT /profile/
Authorization: Bearer <access_token>
{
  "bio": "Hello, I am John",
  "gender": "male",
  "address": "123 Main Street",
  "phone_number": "+1234567890"
}
```

---

### Forgot Password

1. Request OTP:

```bash
POST /forgot-password/
{
  "email": "user@example.com"
}
```

2. Verify OTP:

```bash
POST /forgot-password-verification/
{
  "email": "user@example.com",
  "otp": "123456"
}
```

3. Set New Password:

```bash
POST /set-new-password/
{
  "email": "user@example.com",
  "new_password": "NewPassword123!",
  "confirm_new_password": "NewPassword123!"
}
```

---

## Notes / Best Practices

- OTPs should **expire after 10 minutes**.
- Email sending can be made **asynchronous** using Celery or Django Q.
- Passwords are **hashed** using Django’s default hasher.
- Only **active users** can log in.

---

## Dependencies

- Python 3.10+
- Django 6.x
- Django REST Framework
- djangorestframework-simplejwt
- python-dotenv

Install with:

```bash
pip install django djangorestframework djangorestframework-simplejwt python-dotenv
```

---

## License

MIT License © 2026

```

---

If you want, I can also **generate a ready-to-download `README.md` file** for you with this content so you can directly add it to your project.

Do you want me to do that?
```
