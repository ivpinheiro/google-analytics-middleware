# Google auth imports
from google.oauth2 import service_account
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Utils
import json

class GoogleCloudServicesLogin():
    def __init__(self, key, key_is_path = True):
        self.key = key
        self.key_is_path = key_is_path

    def load_key_file(self):
        if self.key_is_path:
            with open(self.key) as source:
                key_json = json.load(source)
                return key_json
        else:
            key_json = json.loads(self.key)
            return key_json

    def create_google_service_credential_for_ga4(self):
        key_json = self.load_key_file()
        google_creds = service_account.Credentials.from_service_account_info(key_json)
        return google_creds

    def create_google_service_credential_for_ua(self):
        SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
        key_json = self.load_key_file()        
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_json, SCOPES)
        google_creds = build('analyticsreporting', 'v4', credentials=credentials)
        return google_creds