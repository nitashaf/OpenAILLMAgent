import openai
from openai import OpenAI
import json
import requests
import sys


#Simple Agent Class
class Agent:
    def __init__(self, client, model):

        self.client = client
        self.model = model
    
    def handle_user_input(self, user_input):
        
        response = self.client.responses.create(
            model=self.model,
            input=user_input
        )
        return response.output_text

