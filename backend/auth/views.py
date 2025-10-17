from docusign_esign import ApiException
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import redirect

from docusign.ds_client import DsClient
from .session_data import SessionData
from .serializers import CallbackSerializer
from backend.utils import error_processing

@api_view(['GET'])
def health_check(_):
    """
    This is an endpoint that monitoring software can ping to validate
    that our service is still available. And this is a message confirming CI/CD works fine
    """
    return Response({"status": "ok"})

@api_view(['GET'])
def get_status(response):
    """
    Checks if the user is logged in and the type of authentication
    """
    logged = SessionData.is_logged(response.session)
    return Response({"logged": logged})

@api_view(['POST'])
def logout(request):
    """
    Logs out the current user
    """
    request.session.clear()
    return Response({"message": "Logged out"})

@api_view(['GET'])
@error_processing
def code_grant_auth(request):
    """
    The first part of authorizing a user with a OAuth
    """
    url = DsClient.get_redirect_uri()

    return Response({
        'reason': 'Unauthorized',
        'response': 'Redirect to Docusign authorization',
        'url': url
    }, status=401)

@api_view(['POST'])
def callback(request):
    """
    The final part of the user authorization using the OAuth
    """
    serializer = CallbackSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    code = serializer.validated_data['code']

    try:
        auth_data = DsClient.callback(code)
    except ApiException:
        return redirect("jwt_auth")

    SessionData.set_auth_data(request.session, auth_data)
    return Response({"message": "Logged in with code grant"})

@api_view(['POST'])
@error_processing
def jwt_auth(request):
    """
    Endpoint of user authorization using JWT
    """
    try:
        auth_data = DsClient.jwt_auth()

        SessionData.set_auth_data(request.session, auth_data)

        return Response({"message": "Logged in with JWT"})
    except Exception as err:
        print(err.body)
