"""This script compares the .env file in the Google Drive with the local .env file."""
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

_SERVICE_ACCOUNT_FILE = 'drive_key.json'
_SCOPES = ['https://www.googleapis.com/auth/drive']

_CREDENTIALS = service_account.Credentials.from_service_account_file(_SERVICE_ACCOUNT_FILE,
                                                                     scopes=_SCOPES)

_SERVICE = build('drive', 'v3', credentials=_CREDENTIALS)

_FILE_ID = '11XhcOHC_OyfD7FrCEdiJrOj2BKySEHqa'
_FILE_URL = f'https://drive.google.com/file/d/{_FILE_ID}'

def compare_files(file1, file2):
  with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
    return f1.read() == f2.read()

def download_file(file_id, file_name):
  request = _SERVICE.files().get_media(fileId=file_id)
  fh = io.BytesIO()
  downloader = MediaIoBaseDownload(fh, request)

  done = False
  while not done:
    _, done = downloader.next_chunk()
  with open(file_name, 'wb') as f:
    f.write(fh.getbuffer())
  return True

def add_to_gitignore(file_paths):
  with open('.gitignore', 'a+', encoding='utf-8') as gitignore:
    gitignore.seek(0)
    existing_lines = gitignore.read().splitlines()
    gitignore.seek(0, 2)
    for file_path in file_paths:
      if file_path not in existing_lines:
        gitignore.write(f'\n{file_path}')

if __name__ == '__main__':
  download_file_path = 'drive.env'
  local_file_path = '.env'
  add_to_gitignore([download_file_path, local_file_path, _SERVICE_ACCOUNT_FILE])

  if download_file(_FILE_ID, download_file_path):
    if not compare_files(local_file_path, download_file_path):
      print(f'.env file in {_FILE_URL} is different from your local .env file. '\
            'If you update your local .env file, please run the update_env.py '\
            'script with the command python3 hooks_management/update_env.py '\
            f'from the root folder for updating .env file in {_FILE_URL}')
      exit(1)  # Exit with an error code
    else:
      print(f'.env file in {_FILE_URL} is the same as local .env file.')
      exit(0)
  else:
    print('Download failed. Please check your internet connection and try again.')
    exit(1)  # Exit with an error code if download fails
