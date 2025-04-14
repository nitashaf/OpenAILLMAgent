import openai
from openai import OpenAI
import json
import requests
import sys


class weatherAgent:
    
    def __init__(self, client, model):
        
        self.client = client
        self.model = model
    
    
    def get_weather(self,latitude, longitude):
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
        data = response.json()
        return data['current']['temperature_2m']

    
    #adding all steps from the documentation
    
    def handle_user_input(self, user_input):
        input_messages = [{"role": "user", "content": user_input}]
                
        tools = [{
            "type": "function",
            "name": "get_weather",
            "description": "Get current temperature for provided coordinates in celsius.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"}
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False
            },
            "strict": True
        }]
        
        response = self.client.responses.create(
            model=self.model,
            input=input_messages,
            tools=tools,
        )

        tool_call = response.output[0]
        args = json.loads(tool_call.arguments)
        
        result = self.get_weather(args["latitude"], args["longitude"])
        
        input_messages.append(tool_call)
        input_messages.append({
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": str(result)
        })
        
        response_2 = self.client.responses.create(
            model=self.model,
            input=input_messages,
            tools=tools,
        )

        # Return the final output (response)
        return response_2.output_text