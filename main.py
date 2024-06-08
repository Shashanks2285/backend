from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import openai
from dotenv import load_dotenv
import os
import logging

load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

class TodoRequest(BaseModel):
    todos: List[str]

app = FastAPI()

# CORS middleware to allow requests from your React app
app.add_middleware(          
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your React app's URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.post("/api/gpt")
async def ask_gpt(request: TodoRequest):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Here is a list of tasks:\n{'\n'.join(request.todos)}\nWhat can you say about this?",
            max_tokens=150
        )
        logging.info("GPT-3 response: %s", response)
        return {"response": response.choices[0].text.strip()}
    except Exception as e:
        logging.error("Error processing request: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
