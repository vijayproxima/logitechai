import http.client
import json
from dotenv import load_dotenv
load_dotenv()
import os
import json
userQuery=input("")

conn = http.client.HTTPSConnection(os.environ["AZURE_URL"])
payload = json.dumps({
  "messages": [
    {
      "role": "system",
      "content": "You are an AI assistant that helps people find information."
    },
    {
      "role": "user",
      "content": userQuery
    }
  ],
  "temperature": 0.7,
  "top_p": 0.95,
  "frequency_penalty": 0,
  "presence_penalty": 0,
  "max_tokens": 800,
  "stop": None,
  "stream": False
})
headers = {
  'api-key': os.environ['AZURE_API_KEY'],
  'Content-Type': 'application/json'
}
conn.request("POST", "/openai/deployments/LogitechQueryToolDeployment/chat/completions?api-version=2023-07-01-preview", payload, headers)
res = conn.getresponse()

data = res.read()
#print(data.decode("utf-8"))

# Parse the JSON response
response_data = json.loads(data.decode("utf-8"))

# Extract the answer from the "content" field within the "choices" array
answer = response_data['choices'][0]['message']['content']

print(answer)