from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from azure.communication.callautomation import CallAutomationClient
import requests
import os
# from pydantic import BaseModel
# import openai

app = FastAPI() 

TENANT_ID = os.getenv("BOT_TENANT_ID")
CLIENT_ID = os.getenv("BOT_APP_ID")
CLIENT_SECRET = os.getenv("BOT_SECRET")
connection_string = os.getenv("ACS_CONNECTION_STRING")
client = CallAutomationClient.from_connection_string(connection_string)

@app.get("/")
def health():
    return {"status": "voice bot running"}

@app.post("/api/messages")
async def messages(req: Request):
    body = await req.json()
    print(body)
    return {"status": "ok"}

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "https://graph.microsoft.com/.default"
    }

    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()["access_token"]


def answer_call(call_id, token):
    url = f"{GRAPH_BASE}/communications/calls/{call_id}/answer"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "callbackUri": os.getenv("CALLBACK_URI")
    }

    requests.post(url, json=payload, headers=headers)


@app.post("/api/calls")
async def calls_webhook(request: Request):
    data = await request.json()

    print("Incoming webhook:", data)

    token = get_access_token()

    if "value" in data:
        for event in data["value"]:
            resource = event.get("resource", "")
            event_type = event.get("changeType", "")

            if event_type == "created" and "communications/calls" in resource:
                call_id = resource.split("/")[-1]
                print("Incoming call detected:", call_id)

                answer_call(call_id, token)

    return JSONResponse({"status": "ok"})
