from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

import time
import openai
openai.api_key = ''
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Replace with front-end URL
    allow_methods=["GET"],
    allow_headers=["*"],
)
      

@app.get('/')
async def main(prompt: str):
   async def stream_response():
      completion_reason = None
      while not completion_reason or completion_reason == "length":
         openai_stream = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            stream=True,
         )
         for line in openai_stream:
            completion_reason = line["choices"][0]["finish_reason"]
            if "content" in line["choices"][0].delta:
               current_response = line["choices"][0].delta.content
               yield current_response
   return StreamingResponse(stream_response(), media_type='text/event-stream')