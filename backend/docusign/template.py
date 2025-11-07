from docusign_esign import TemplatesApi, Recipients, EnvelopeTemplate

from docusign.ds_client import DsClient
from docusign.document import create_document

from .templates.make_request_medical_records_signer import make_request_medical_records_signer
from .templates.make_covid_19_consent_form_signer import make_covid_19_consent_form_signer
from .templates.make_application_for_participation_signer import make_application_for_participation_signer

class Template:

    @staticmethod
    def get_existing(templates_api, account_id, template_request_object):
        """
        Returns the ID of the template if such a template already exists
        """
        templates = templates_api.list_templates(account_id)
        for template in templates.envelope_templates:
            if template.name == template_request_object.name:
                return template.template_id
        return None

    @classmethod
    def create(cls, session, template_request_object):
        """
        Create a template
        """
        api_client = DsClient.get_configured_instance(
            access_token=session["access_token"]
        )
        templates_api = TemplatesApi(api_client)
        account_id=session["account_id"]

        existing_template_id = cls.get_existing(templates_api, account_id, template_request_object)
        if existing_template_id is not None:
            print("Using the existing template.")
            return existing_template_id

        template = templates_api.create_template(
            account_id=account_id,
            envelope_template=template_request_object
        )
        return template.template_id

    @staticmethod
    def make_request(template_name, document, signer):
        """
        Make a template request
        """
        return EnvelopeTemplate(
            documents=[document],
            email_subject="Please sign this document",
            recipients=Recipients(signers=[signer]),
            description="Example template created via the Healthcare Sample App",
            name=template_name,
            shared="false",
            status="sent"
        )

    @classmethod
    def make_request_medical_records(cls, workflow_id, args):
        """
        Make template_request for request_medical_records endpoint
        """
        template_name = "RequestMedicalRecordsTemplate"
        document = create_document("Medical_release_form.pdf")
        signer = make_request_medical_records_signer(workflow_id, args)

        return cls.make_request(template_name, document, signer)

    @classmethod
    def make_covid_19_consent_form(cls, args):
        """
        Make template_request for covid19_consent endpoint
        """
        template_name = "Covid19ConsentFormTemplate"
        document = create_document("COVID19-consent.pdf")
        signer = make_covid_19_consent_form_signer(args)

        return cls.make_request(template_name, document, signer)

    @classmethod
    def make_application_for_participation(cls, args, session):
        """
        Make template_request for application_for_participation endpoint
        """
        template_name = "ApplicationForParticipationTemplate"
        document = create_document("Application_for_participation_v2.pdf")
        signer = make_application_for_participation_signer(args, session)

        return cls.make_request(template_name, document, signer)
