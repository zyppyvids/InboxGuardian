import os.path
import base64
from pathlib import Path
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(Path(f"{os.getcwd()}\\sensitive_data\\token.json")):
        creds = Credentials.from_authorized_user_file(Path(f"{os.getcwd()}\\sensitive_data\\token.json"), SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                Path(f"{os.getcwd()}\\sensitive_data\\credentials.json"), SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(Path(f"{os.getcwd()}\\sensitive_data\\token.json"), "w") as token:
                token.write(creds.to_json())
    # Gathering spam emails and parsing them
    try:
        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(userId='me', labelIds=['SPAM'], q="").execute()
        messages = results.get('messages', [])

        try:
            os.mkdir(f"{os.getcwd()}\\files\\")
            print("Created directory 'files'.")
        except:
            print("Directory 'files' already exists, continuing ahead...")

        if not messages:
            print('No spam messages found.')
        else:
            message_count = 0
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                email_data = msg['payload']['headers']
                for values in email_data:
                    name = values['name']
                    if name == 'From':
                        try:
                            data = msg['payload']['body']['data']
                            data = data.replace("-","+").replace("_","/")
                            decoded_data = base64.b64decode(data)
                            soup = BeautifulSoup(decoded_data , "lxml")
                            text = soup.get_text()
                            filtered_text = '\n'.join(list(line.strip().replace('\u200C', '').replace('\u00A0', '') for line in filter(lambda line: line.strip().replace('\u200C', '').replace('\u00A0', '') != '', text.split('\n')))).replace('\n', ' ')

                            with open(Path(f"{os.getcwd()}\\files\\{msg['id']}.txt"), "w", encoding="utf-8") as writer:
                                writer.write(filtered_text)
                                
                            with open(Path(f"{os.getcwd()}\\..\\data\\spam_1.csv"), "a", encoding="utf-8") as writer:
                                filtered_text = filtered_text.replace('"',"'")
                                writer.write(f"spam,\"{filtered_text}\"\n")

                            message_count += 1
                        except Exception as error:
                            print(f"Skipping a message...")
    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()