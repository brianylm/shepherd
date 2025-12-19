import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("ERROR: credentials.json not found. Please download it from Google Cloud Console.")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def search_shipping_emails(service):
    """
    Search for emails from specific senders with shipping keywords.
    """
    query = "from:(Lazada OR Shopee OR Amazon OR Keychron) subject:(shipping OR shipped)"
    results = service.users().messages().list(userId='me', q=query, maxResults=10).execute()
    messages = results.get('messages', [])
    return messages

def get_email_body(service, msg_id):
    """
    Get the body of the email. Prefer plain text, then html.
    """
    message = service.users().messages().get(userId='me', id=msg_id).execute()
    payload = message.get('payload', {})
    parts = payload.get('parts', [])
    data = None
    
    if not parts:
        # Simple message
        data = payload.get('body', {}).get('data')
    else:
        # Multipart message
        for part in parts:
            if part.get('mimeType') == 'text/plain':
                data = part.get('body', {}).get('data')
                break
        if not data:
             for part in parts:
                if part.get('mimeType') == 'text/html':
                    data = part.get('body', {}).get('data')
                    break
    
    if data:
        return base64.urlsafe_b64decode(data).decode('utf-8')
    return ""
