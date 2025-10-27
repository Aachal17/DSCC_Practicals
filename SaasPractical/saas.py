import os
import io
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
# Google Drive API scope for full access
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'
def authenticate_google_drive():
 """Authenticate and return the Google Drive service"""
 creds = None
 try:
 # Load existing credentials
 if os.path.exists(TOKEN_FILE):
 creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
 # Refresh or generate new credentials if needed
 if not creds or not creds.valid:
 if creds and creds.expired and creds.refresh_token:
 creds.refresh(Request())
 else:
 # Use InstalledAppFlow for Desktop client type
 flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE,
SCOPES)
 creds = flow.run_local_server(port=8080, prompt='consent')
 # Save new credentials for future runs
 with open(TOKEN_FILE, 'w') as token:
 token.write(creds.to_json())
 return build('drive', 'v3', credentials=creds)
 except Exception as e:
 print(f"Authentication failed: {e}")
 sys.exit(1)
def upload_file(file_path):
 """Upload a file to Google Drive"""
 try:
 service = authenticate_google_drive()
 file_metadata = {'name': os.path.basename(file_path)}
 media = MediaFileUpload(file_path, resumable=True)
 file = service.files().create(body=file_metadata, media_body=media,
fields='id').execute()
 print(f"File uploaded successfully. File ID: {file.get('id')}")
 except Exception as e:
 print(f"Upload failed: {e}")
def list_files():
 """List first 10 files from Google Drive"""
 try:
 service = authenticate_google_drive()
 results = service.files().list(pageSize=10, fields="files(id, name)").execute()
 items = results.get('files', [])
 if not items:
 print('No files found.')
 else:
 print("Files in your Drive:")
 for item in items:
 print(f"- {item['name']} (ID: {item['id']})")
 except Exception as e:
 print(f"Listing files failed: {e}")
def download_file(file_id, save_as):
 """Download a file from Google Drive"""
 try:
 service = authenticate_google_drive()
 request = service.files().get_media(fileId=file_id)
 fh = io.FileIO(save_as, 'wb')
 downloader = MediaIoBaseDownload(fh, request)
 done = False
 while not done:
 status, done = downloader.next_chunk()
 print(f"Download progress: {int(status.progress() * 100)}%")
 print(f"File downloaded and saved as: {save_as}")
 except Exception as e:
 print(f"Download failed: {e}")
def delete_file(file_id):
 """Delete a file from Google Drive"""
 try:
 service = authenticate_google_drive()
 service.files().delete(fileId=file_id).execute()
 print(f"File with ID {file_id} deleted successfully.")
 except Exception as e:
 print(f"Delete failed: {e}")
def main_menu():
 while True:
 print("\nGoogle Drive Storage as a Service Menu")
 print("1. Upload File\n2. List Files\n3. Download File\n4. Delete File\n5. Exit")
 choice = input("Enter your choice (1-5): ").strip()
 if choice == '1':
 path = input("Enter file path to upload: ").strip()
 if os.path.exists(path):
 upload_file(path)
 else:
 print("File not found.")
 elif choice == '2':
 list_files()
 elif choice == '3':
 file_id = input("Enter File ID to download: ").strip()
 save_path = input("Enter file name to save as: ").strip()
 download_file(file_id, save_path)
 elif choice == '4':
 file_id = input("Enter File ID to delete: ").strip()
 delete_file(file_id)
 elif choice == '5':
 print("Exiting. Thank you!")
 break
 else:
 print("Invalid choice. Please select between 1 and 5.")
if __name__ == '__main__':
 main_menu