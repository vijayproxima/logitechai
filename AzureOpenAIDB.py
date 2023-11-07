import openai
from dotenv import load_dotenv
load_dotenv()

import os

openai.api_type = "azure"
openai.api_base = "https://resourceforazureopenaidemo.openai.azure.com/"
openai.api_version = "2023-05-15"
openai.api_key = 'cfb9b2ee9f43405a944adaf03727d04c'
deployment_name="gpt-35-turbo"
def get_completion_from_messages(system_message, user_message, temperature=0, max_tokens=500) -> str:

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{user_message}"}
    ]
    
    response = openai.ChatCompletion.create(
        engine=deployment_name,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    
    return response.choices[0].message["content"]

if __name__ == "__main__":
    system_message = "You are a helpful assistant"
    user_message = "what is the capital of india?"
    print(get_completion_from_messages(system_message, user_message))