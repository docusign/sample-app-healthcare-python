import requests
from docusign_esign import ExtensionData, ConnectionInstance
from docusign.ds_config import SMARTY_EXTENSION_ID, PHONE_EXTENSION_ID, SSN_EXTENSION_ID, CONNECTED_FIELDS_BASE_HOST

class Extensions:
    @staticmethod
    def get_extension_apps(session):
        headers = {
            "Authorization": "Bearer " + session['access_token'],
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        url = f"{CONNECTED_FIELDS_BASE_HOST}/v1/accounts/{session['account_id']}/connected-fields/tab-groups"
        response = requests.get(url, headers=headers)
        
        return response.json()

    def get_extension_app(session, appId):
        headers = {
            "Authorization": "Bearer " + session['access_token'],
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        url = f"{CONNECTED_FIELDS_BASE_HOST}/v1/accounts/{session['account_id']}/connected-fields/tab-groups?appId={appId}"
        response = requests.get(url, headers=headers)

        return response.json()

    @staticmethod
    def get_address_extension_id():
        return SMARTY_EXTENSION_ID

    @staticmethod
    def get_phone_extension_id():
        return PHONE_EXTENSION_ID
    
    @staticmethod
    def get_ssn_extension_id():
        return SSN_EXTENSION_ID
    
    @staticmethod
    def get_extension_by_app_id(objects, app_id):
        return next((obj for obj in objects if obj["appId"] == app_id), None)
    
    @staticmethod
    def extract_verification_data(selected_app_id, tab):
        extension_data = tab["extensionData"]

        return {
            "app_id": selected_app_id,
            "extension_group_id": extension_data["extensionGroupId"] if "extensionGroupId" in extension_data else "",
            "publisher_name": extension_data["publisherName"] if "publisherName" in extension_data else "",
            "application_name": extension_data["applicationName"] if "applicationName" in extension_data else "",
            "action_name": extension_data["actionName"] if "actionName" in extension_data else "",
            "action_input_key": extension_data["actionInputKey"] if "actionInputKey" in extension_data else "",
            "action_contract": extension_data["actionContract"] if "actionContract" in extension_data else "",
            "extension_name": extension_data["extensionName"] if "extensionName" in extension_data else "",
            "extension_contract": extension_data["extensionContract"] if "extensionContract" in extension_data else "",
            "required_for_extension": extension_data["requiredForExtension"] if "requiredForExtension" in extension_data else "",
            "tab_label": tab["tabLabel"],
            "connection_key": (
                extension_data["connectionInstances"][0]["connectionKey"]
                if "connectionInstances" in extension_data and extension_data["connectionInstances"]
                else ""
            ),
            "connection_value": (
                extension_data["connectionInstances"][0]["connectionValue"]
                if "connectionInstances" in extension_data and extension_data["connectionInstances"]
                else ""
            )
        }

    @staticmethod
    def get_extension_data(verification_data):
        return ExtensionData(
            extension_group_id = verification_data["extension_group_id"],
            publisher_name = verification_data["publisher_name"],
            application_id = verification_data["app_id"],
            application_name = verification_data["application_name"],
            action_name = verification_data["action_name"],
            action_contract = verification_data["action_contract"],
            extension_name = verification_data["extension_name"],
            extension_contract = verification_data["extension_contract"],
            required_for_extension = verification_data["required_for_extension"],
            action_input_key = verification_data["action_input_key"],
            extension_policy = 'MustVerifyToSign',
            connection_instances = [ConnectionInstance(
                connection_key = verification_data["connection_key"],
                connection_value = verification_data["connection_value"],
            )]
        )