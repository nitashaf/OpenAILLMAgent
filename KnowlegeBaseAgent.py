import openai
from openai import OpenAI
import json
import requests
import sys
from config import test_api_key, test_client, test_model



class knowlegeBaseAgent:
    
    def __init__(self, client, model):
        
        self.client = client
        self.model = model
        self.api_key = test_api_key
        self.file_id = None
        self.upload_file_to_openai()
        self.assistant_id = None
        
    def upload_file_to_openai(self):
        filepath="s11704-024-40490-y.pdf"
        api_key=test_api_key 
        purpose="assistants"

        url = "https://api.openai.com/v1/files"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        files = {
            "file": open(filepath, "rb")
        }
        data = {
            "purpose": purpose
        }

        response = requests.post(url, headers=headers, files=files, data=data)

        if response.status_code == 200:
            #print("File uploaded successfully!")
            result = response.json()
            self.file_id = result.get("id")  
        else:
            print(f"Failed to upload. Status code: {response.status_code}")
            print(response.text)
        
    def get_paper_response(self, user_input):
        url = "https://api.openai.com/v1/responses"
    
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": 'gpt-4o',
            "input": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_file",
                            "file_id": self.file_id
                        },
                        {
                            "type": "input_text",
                            "text": user_input
                        }
                    ]
                }
            ]
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(response.text)


    def handle_user_input(self, user_input):
        
        result = self.get_paper_response(user_input)
        
        return result['output'][0]['content'][0]['text']
