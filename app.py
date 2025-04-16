import json
from fastapi import FastAPI, HTTPException
import httpx

# Initialize the FastAPI app
app = FastAPI()

# Vapi API URL
VAPI_API_URL = "https://api.vapi.ai/assistant"

# Your Authorization Token for Vapi
VAPI_AUTH_TOKEN = "<your_vapi_auth_token>"

# HTTP Client for making requests to Vapi API
client = httpx.AsyncClient()

# Function to create assistant on Vapi API
async def create_vapi_assistant(payload: dict):
    headers = {
        "Authorization": f"Bearer {VAPI_AUTH_TOKEN}",
        "Content-Type": "application/json",
    }
    response = await client.post(VAPI_API_URL, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code != 201:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error: {response.text}",
        )
    
    return response.json()

# Endpoint to create assistant
@app.post("/create_assistant")
async def create_assistant(data: dict):
    """
    Endpoint to create an assistant using the Vapi API.
    :param data: The incoming data to create an assistant.
    :return: JSON response from Vapi API.
    """
    
    # Transform incoming data (you may add logic here for Retell AI-specific data)
    assistant_payload = {
        "name": data.get("name", "DefaultAssistant"),
        "firstMessage": data.get("firstMessage", "Hello! How can I assist you today?"),
        "firstMessageMode": data.get("firstMessageMode", "assistant-speaks-first"),
        "voice": data.get("voice", {}),
        "model": data.get("model", {}),
        "transcriber": data.get("transcriber", {}),
        "maxDurationSeconds": data.get("maxDurationSeconds", 600),
        "silenceTimeoutSeconds": data.get("silenceTimeoutSeconds", 30)
    }

    # Make a request to Vapi to create the assistant
    response = await create_vapi_assistant(assistant_payload)

    return response
