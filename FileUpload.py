    from config import test_api_key, test_client, test_model

    result = None
    def upload_file_to_openai():
        filepath="C:\\Users\\nitas\\Downloads\\s11704-024-40490-y.pdf"
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
            print("File uploaded successfully!")
            return response.json()
        else:
            print(f"Failed to upload. Status code: {response.status_code}")
            print(response.text)
            return None
            
    def get_get_paper_response(user_input):
        url = "https://api.openai.com/v1/responses"
    
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {test_api_key}"
        }

        payload = {
            "model": 'gpt-4o',
            "input": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_file",
                            "file_id": 'file-WLDHZ49p6efHfpAZeTe21m'
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
            print(result['output'][0]['content'][0]['text'])

        else:
            print(response.text)
            return None    
        
        
    upload_file_to_openai()
    #get_get_paper_response("What is this paper about ?")
