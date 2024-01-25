"""
This script updates the .env file on Google Drive with the local .env file.
"""
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO

# Path to your service account key
SERVICE_ACCOUNT_FILE = 'drive_key.json'

# Scopes for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

# Initialize credentials
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Drive API service
service = build('drive', 'v3', credentials=credentials)

# ID of the .env file on Google Drive you want to update
_FILE_ID = '11XhcOHC_OyfD7FrCEdiJrOj2BKySEHqa'

# Path to the local .env file you want to upload
local_env_path = '.env'

# Read the content from the local .env file
with open(local_env_path, 'r', encoding='utf-8') as file:
  local_env_content = file.read()

# Prepare the content for uploading
fh = BytesIO(local_env_content.encode())
media = MediaIoBaseUpload(fh, mimetype='text/plain')

# Update the .env file on Google Drive
updated_file = service.files().update(
    fileId=_FILE_ID,
    media_body=media).execute()

print('Updated .env file in Google Drive with the content from your local .env')
