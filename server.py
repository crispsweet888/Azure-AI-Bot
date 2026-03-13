from fastapi import FastAPI, Request
from azure.communication.callautomation import CallAutomationClient
import os
# from pydantic import BaseModel
# import openai

app = FastAPI() 

connection_string = os.getenv("ACS_CONNECTION_STRING")
client = CallAutomationClient.from_connection_string(connection_string)

@app.get("/")
def health():
    return {"status": "running"}

@app.post("/api/messages")
async def messages(req: Request):
    body = await req.json()
    print(body)
    return {"status": "ok"}

@app.post("/api/call")
async def handle_event(req: Request):
    events = await req.json()
    event = events[0]

    if event["eventType"] == "Microsoft.Communication.IncomingCall":
        incoming_call_context = event["data"]["incomingCallContext"]

        client.answer_call(
            incoming_call_context=incoming_call_context,
            callback_url="https://jjs-ai-voice-bot-dehnh5dzehcxfdf2.canadaeast-01.azurewebsites.net/api/callback"
        )

    return {"status": "ok"}

@app.post("/api/callback")
async def callback(req: Request):
    body = await req.json()
    print("call event:", body)
    return {"status": "ok"}

# class VoiceInput(BaseModel):
#     text: str

# @app.post("/voice-intent")
# async def voice_intent(data: VoiceInput):

#     prompt = f"""
#     Classify the request.

#     Request: {data.text}

#     Categories:
#     - customer_service
#     - technical_support
#     - billing
#     - general_question
#     """

#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[{"role":"user","content":prompt}]
#     )

#     return {"intent": response["choices"][0]["message"]["content"]}