import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import List

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailReader:
    def __init__(self, token_path: str = 'token.json', creds_path: str = 'credentials.json'):
        self.creds = None
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('gmail', 'v1', credentials=self.creds)

    def search_by_subject(self, subject: str) -> List[dict]:
        query = f'subject:{subject}'
        results = self.service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        emails = []
        for msg in messages:
            msg_data = self.service.users().messages().get(userId='me', id=msg['id']).execute()
            snippet = msg_data.get('snippet', '')
            emails.append({'id': msg['id'], 'snippet': snippet})
        return emails

if __name__ == "__main__":
    reader = GmailReader()
    subject = input("Enter subject to search: ")
    emails = reader.search_by_subject(subject)
    for email in emails:
        print(f"ID: {email['id']}, Snippet: {email['snippet']}")