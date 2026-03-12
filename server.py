from fastapi import FastAPI, Request
# from pydantic import BaseModel
# import openai

app = FastAPI()

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
    body = await req.json()

    # Event Grid sends events as a list
    if isinstance(body, list):
        event = body[0]

        # Handle Event Grid validation
        if event.get("eventType") == "Microsoft.EventGrid.SubscriptionValidationEvent":
            code = event["data"]["validationCode"]
            return {"validationResponse": code}

    print("Received event:", body)
    return {"status": "received"}

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