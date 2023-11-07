import os
import requests
from dotenv import load_dotenv

load_dotenv()

userQuery = input("Enter your query: ")

# Define the Bot Framework endpoint and API version
bot_endpoint = os.environ["BOT_ENDPOINT"]
api_version = "V1.3"

# Define the authentication credentials
bot_app_id = os.environ["BOT_APP_ID"]
bot_app_password = os.environ["BOT_APP_PASSWORD"]

# Compose the request URL
bot_url = f"{bot_endpoint}/v{api_version}/conversations/{bot_app_id}/activities"

# Define the message payload
message = {
    "type": "message",
    "from": {"id": bot_app_id},
    "text": userQuery,
}

# Send the message to the bot
headers = {
    "Authorization": f"Bearer {bot_app_password}",
    "Content-Type": "application/json",
}

response = requests.post(bot_url, headers=headers, json=message)

if response.status_code == 200:
    bot_response = response.json()
    answer = bot_response.get("text")
    print("Bot Response:", answer)
else:
    print("Failed to communicate with the bot. Status code:", response.status_code)
