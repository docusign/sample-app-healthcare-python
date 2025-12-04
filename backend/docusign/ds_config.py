import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_EXPIRATION_IN_SECONDS = 3600
TOKEN_REPLACEMENT_IN_SECONDS = 10 * 60

CODE_GRANT_SCOPES = ['signature', 'click.manage', 'adm_store_unified_repo_read']
PERMISSION_SCOPES = ['signature', 'impersonation', 'click.manage', 'adm_store_unified_repo_read']

CONNECTED_FIELDS_BASE_HOST = 'https://api-d.docusign.com'
PHONE_EXTENSION_ID = "d16f398f-8b9a-4f94-b37c-af6f9c910c04"
SMARTY_EXTENSION_ID = "04bfc1ae-1ba0-42d0-8c02-264417a7b234"
SSN_EXTENSION_ID = "b1adf7ad-38fd-44ba-85f5-38ea87f4af23"

DS_RETURN_URL = os.environ.get('REACT_APP_DS_RETURN_URL')
DS_AUTH_SERVER = os.environ.get('DS_AUTH_SERVER')
DS_DEMO_SERVER = os.environ.get('DS_DEMO_SERVER')

DJANGO_SECRET = os.environ.get('DJANGO_SECRET')

PATH_TO_PRIVATE_KEY_FILE = "private.key"

with open(PATH_TO_PRIVATE_KEY_FILE) as private_key_file:
    private_key = private_key_file.read()

PRIVATE_KEY = private_key