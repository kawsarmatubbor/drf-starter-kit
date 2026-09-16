from rest_framework.response import Response
from rest_framework import status

# Success response
def success(status_code=status.HTTP_200_OK, message="Success", data=None):
    return Response({
        "status": status_code,
        "success": True,
        "message": message,
        "data": data,
    }, status=status_code)

# Error response
def error(status_code=status.HTTP_400_BAD_REQUEST, message="Error", errors=None):
    return Response({
        "status": status_code,
        "success": False,
        "message": message,
        "data": None,
        "errors": errors
    }, status=status_code)