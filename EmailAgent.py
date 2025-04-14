import openai
from openai import OpenAI
import json
import requests
import sys
import base64
from email.mime.text import MIMEText
import html
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

    
class emailAgent:
    
    def __init__(self, client, model):
        
        self.client = client
        self.model = model
        self.service = self.authenticate_gmail()
    
    
    def authenticate_gmail(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    
    def read_email(self, limit=5):
        result = self.service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=limit).execute()
        messages = result.get('messages', [])

        if not messages:
            return "No unread emails."

        summary = []
        for msg in messages:
            msg_data = self.service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = msg_data['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown sender')
            snippet = msg_data.get('snippet', '')[:300]

            # Decode HTML entities like &#39;
            subject = html.unescape(subject)
            sender = html.unescape(sender)
            snippet = html.unescape(snippet)

            summary.append(f" **From:** {sender}\n**Subject:** {subject}\n**Snippet:** {snippet.strip()}\n{'-'*60}")

        return "\n".join(summary)
    
    
    def send_email(self, to: str, subject: str, body: str) -> str:
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message = {'raw': raw}

        self.service.users().messages().send(userId='me', body=message).execute()

        return f"Email sent to {to}."

    
    
    def handle_user_input(self, user_input):
        tools = [
            {
                "type": "function",
                "name": "send_email",
                "description": "Send an email to a given recipient with a subject and message.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to": {"type": "string"},
                        "subject": {"type": "string"},
                        "body": {"type": "string"}
                    },
                    "required": ["to", "subject", "body"]
                }
            },
            {
                "type": "function",
                "name": "read_email",
                "description": "List top 5 new emails.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "default": 5}
                    }
                }
            }
        ]

        input_messages = [{"role": "user", "content": user_input}]
        stream = self.client.responses.create(
            model=self.model,
            input=input_messages,
            tools=tools,
            stream=True
        )

        # Step 1: Collect tool call deltas
        final_tool_calls = {}

        for event in stream:
            if event.type == 'response.output_item.added':
                final_tool_calls[event.output_index] = event.item;
            elif event.type == 'response.function_call_arguments.delta':
                index = event.output_index

                if final_tool_calls[index]:
                    final_tool_calls[index].arguments += event.delta

        # Step 2: Call the tool
        for index, tool_call in final_tool_calls.items():
            args = json.loads(tool_call.arguments)

            if tool_call.name == "send_email":
                result = self.send_email(**args)
            elif tool_call.name == "read_email":
                result = self.read_email(**args)
            else:
                result = "Unknown tool requested."

            # Append tool call + output
            input_messages.append({
                "type": "function_call",
                "call_id": tool_call.call_id,
                "name": tool_call.name,
                "arguments": tool_call.arguments
            })

            input_messages.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": str(result)
            })

        # Step 4: Final response from GPT
        final_response = self.client.responses.create(
            model=self.model,
            input=input_messages,
            tools=tools
        )

        return final_response.output_text
