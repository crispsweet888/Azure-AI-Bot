from fastapi import FastAPI, Request
# from pydantic import BaseModel
# import openai

app = FastAPI()

@app.get("/")
def health():
    return {"status": "running"}

# @app.post("/api/messages")
# async def messages(req: Request):
#     body = await req.json()
#     print(body)
#     return {"status": "ok"}

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