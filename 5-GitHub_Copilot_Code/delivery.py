# delivery.py
import secrets

from models import RequestStatus


def generate_otp():
    """FR-005: generate a 4-digit OTP."""
    return f"{secrets.randbelow(10000):04d}"


def complete_delivery(request, entered_otp):
    """
    FR-005:
    Mark the request Delivered only when the entered OTP matches exactly.
    """
    if request.otp is None:
        return False
    if str(entered_otp) == str(request.otp):
        request.status = RequestStatus.Delivered.value
        return True
    return False
