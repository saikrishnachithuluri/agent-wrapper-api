from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
RETELL_API_KEY = os.getenv("RETELL_API_KEY")

# Define the common input schema
class AssistantRequest(BaseModel):
    provider: str  # "vapi" or "retell"
    name: str
    voice_id: str
    language: str = "en-US"
    first_message: str

@app.post("/create_assistant")
def create_assistant(data: AssistantRequest):
    if data.provider == "vapi":
        return create_vapi_assistant(data)
    elif data.provider == "retell":
        return create_retell_assistant(data)
    else:
        raise HTTPException(status_code=400, detail="Invalid provider. Must be 'vapi' or 'retell'.")

def create_vapi_assistant(data: AssistantRequest):
    url = "https://api.vapi.ai/assistant"
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": data.name,
        "voice": {
            "provider": "11labs",
            "voiceId": data.voice_id
        },
        "language": data.language,
        "firstMessage": data.first_message,
        "firstMessageMode": "assistant-speaks-first"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Vapi error: {response.text}")

def create_retell_assistant(data: AssistantRequest):
    url = "https://api.retellai.com/agent"  # Replace with correct endpoint
    headers = {
        "Authorization": f"Bearer {RETELL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "agent_name": data.name,
        "response_engine": {
            "type": "retell-llm",
            "llm_id": "llm_234sdertfsdsfsdf"
        },
        "voice_id": data.voice_id,
        "language": data.language,
        "voicemail_message": data.first_message
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Retell error: {response.text}")
