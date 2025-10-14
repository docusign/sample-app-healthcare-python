import requests
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
        }

    @staticmethod
    def get_extension_data(verification_data):
        return {
            "extensionGroupId": verification_data["extension_group_id"],
            "publisherName": verification_data["publisher_name"],
            "applicationId": verification_data["app_id"],
            "applicationName": verification_data["application_name"],
            "actionName": verification_data["action_name"],
            "actionContract": verification_data["action_contract"],
            "extensionName": verification_data["extension_name"],
            "extensionContract": verification_data["extension_contract"],
            "requiredForExtension": verification_data["required_for_extension"],
            "actionInputKey": verification_data["action_input_key"],
            "extensionPolicy": 'MustVerifyToSign'
        }