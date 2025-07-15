import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from typing import List

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailAPI:
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

    def send_email(self, to: str, subject: str, body: str, attachments: List[str] = None) -> str:
        """Send an email with optional attachments using the Gmail API."""
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        import base64
        import os
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    part = MIMEBase('application', 'octet-stream')
                    with open(file_path, 'rb') as f:
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
                    message.attach(part)
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        try:
            sent = self.service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
            return f"Email sent! ID: {sent['id']}"
        except Exception as e:
            return f"Error sending email: {e}"

if __name__ == "__main__":
    reader = GmailAPI()
    action = input("Type 'search' to search by subject or 'send' to send an email: ").strip().lower()
    if action == 'search':
        subject = input("Enter subject to search: ")
        emails = reader.search_by_subject(subject)
        for email in emails:
            print(f"ID: {email['id']}, Snippet: {email['snippet']}")
    elif action == 'send':
        to = input("Recipient email: ")
        subject = input("Email subject: ")
        body = input("Email body: ")
        attach_input = input("Attachment file paths (comma separated, or leave blank): ")
        attachments = [a.strip() for a in attach_input.split(',')] if attach_input else None
        result = reader.send_email(to, subject, body, attachments)
        print(result)