from rest_framework.response import Response
from rest_framework import status

# Success response
def success(data=None, message="Success", status_code=status.HTTP_200_OK):
    return Response({
        "success": True,
        "message": message,
        "data": data,
        "status": status_code,
    }, status=status_code)

# Error response
def error(message="Error", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "success": False,
        "message": message,
        "data": None,
        "status": status_code,
        "errors": errors
    }, status=status_code)