import random


# Generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))
