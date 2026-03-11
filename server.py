from fastapi import FastAPI
from pydantic import BaseModel
import openai

app = FastAPI()

@app.get("/")
def root():
    return {"status": "AI voice bot running"}

class VoiceInput(BaseModel):
    text: str

@app.post("/voice-intent")
async def voice_intent(data: VoiceInput):

    prompt = f"""
    Classify the request.

    Request: {data.text}

    Categories:
    - customer_service
    - technical_support
    - billing
    - general_question
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}]
    )

    return {"intent": response["choices"][0]["message"]["content"]}