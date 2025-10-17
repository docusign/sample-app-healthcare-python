import os
from rest_framework.response import Response
from rest_framework.decorators import api_view

from docusign.template import Template
from docusign.envelope import Envelope
from docusign.workflow import get_idv_workflow, is_sms_workflow
from docusign.extensions import Extensions

from .serializers import (
    RequestMedicalRecordsSerializer,
    Covid19ConsentFormSerializer,
    ApplyForPatientAssistanceSerializer
)
from backend.utils import error_processing

@api_view(['POST'])
@error_processing
def request_medical_records(request):
    """
    The Request Medical Records flow
    """
    serializer = RequestMedicalRecordsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    workflow_id = get_idv_workflow(request.session)

    if workflow_id is None:
        return Response({
            "message": "IDV not enabled in your account"
        })
    args = serializer.validated_data.copy()

    template_request = Template.make_request_medical_records(workflow_id, args)
    template_id = Template.create(request.session, template_request)

    args["template_id"] = template_id
    envelope_definition = Envelope.create_request_medical_records_definition(args)

    Envelope.send(request.session, envelope_definition)

    return Response({"message": "successfully sent request"})

@api_view(['POST'])
@error_processing
def covid19_consent_form(request):
    """
    The COVID-19 Consent Form flow
    """
    serializer = Covid19ConsentFormSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    args = serializer.validated_data.copy()

    if is_sms_workflow(request.session) == "false":
        return Response({
            "message": "SMS option is not enabled in your account"
        })

    template_request = Template.make_covid_19_consent_form(args)
    template_id = Template.create(request.session, template_request)

    args["template_id"] = template_id
    envelope_definition = Envelope.create_covid_19_consent_form_definition(args)

    Envelope.send(request.session, envelope_definition)

    return Response({"message": "successfully sent request"})

@api_view(['POST'])
@error_processing
def apply_for_patient_assistance(request):
    """
    The Apply for Patient Assistance flow
    """
    try:
        serializer = ApplyForPatientAssistanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        args = serializer.validated_data.copy()

        template_request = Template.make_application_for_participation(args, request.session)
        template_id = Template.create(request.session, template_request)
        print(f"Template ID: {template_id}")

        args["template_id"] = template_id

        envelope_definition = Envelope.create_application_for_participation_definition(args)

        envelope_id = Envelope.send(request.session, envelope_definition)
        view_url = Envelope.get_view_url(request.session, envelope_id, args)

        return Response({"view_url": view_url, "client_id": os.environ.get('CLIENT_ID')})
    except Exception as err:
        print(err)

@api_view(['GET'])
@error_processing
def get_extension_apps(request):
    """
    Retrieve the list of extensions
    """
    try:
        extensions = Extensions.get_extension_apps(request.session)
        actual_extension_app_ids = [item["appId"] for item in extensions]
        actual_apps = [{ "name": app["tabs"][0]["extensionData"]["applicationName"], "appId": app["appId"]} for app in extensions]
        print("Installed apps:")
        print(actual_apps)

        required_ids = {
            Extensions.get_address_extension_id(),
            Extensions.get_phone_extension_id(),
            Extensions.get_ssn_extension_id(),
        }
        print("Required apps:")
        print(required_ids)

        has_all_app_ids = all(app_id in actual_extension_app_ids for app_id in required_ids)

        return Response({"areExtensionsPresent": has_all_app_ids})
    except Exception as err:
        print(err)
