"""
This is  a FastAPI project that integrates with Gemini for a chatbot on Woocommerce site
It must scrape the site for available products, then pass same info to the chatbot
which is powered by Gemini
Must use CORS...so client's domain can speak to my backend service which is
likely to be hosted on a 3rd party server? e.g: Render or Replit
GPT has voted for Render as the best option

Building a basic API backend that exposes a 'chat' endpoint to our users.
User can send whatever text they want, backend will use the model to answer
We'll use a Rate Limiter to prevent user from sending too many requests
RL allows me to control the amount of traffic I let through--necessary to not exhaust
free API tokens or rack up avoidable costs

pip install "fastapi[standard]" pydantic google-genai slowapi
pip install -q packagename installs the libs without any extra noise
literally means install quietly
with the standard fastapi package everything else comes with: pydantic, uvicorn. starlette
fastapi: API framework
uvicorn: web server runtime to run and host app locally for easy testing
pydantic: for data validation & serialization, makes using API inputs and outputs easier
google-generativeai: AI client to access gemini API
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from google import genai
from google.genai import types
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import List, Dict
from rag import fetch_products
import json

load_dotenv()



limiter = Limiter(key_func=get_remote_address)
# ---- App Initialization ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
#app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client (reads GEMINI_API_KEY from env var)
client = genai.Client()

#Define the request and response models
class ChatRequest(BaseModel):
    prompt: str  #we expect a JSON body like {"prompt": "..."}

class ChatResponse(BaseModel):
    answer: str #we'll return a JSON body like {"response": "..."}
    products: List[Dict] = [] #returns empty list if no products are found matching prompt


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"message": "This API relies on a free AI model. Only 2 requests per minute allowed globally."}
    )

#root endpoint doesn't really do anything. just gives us a health check
@app.get("/")
async def root():
    return {"message": "API is running"}

#can test the project by running this: uvicorn main:app --reload #reload makes it reload when changes
#if main.py file is in src sub-folder.. uvicorn src.main:app --reload

@app.post("/chat", response_model=ChatResponse)
@limiter.limit("2/minute", key_func=lambda request: "global")
#response_model param tells FastAP to return a response that matches the ChatResponse structure
#we'll run the function below when a request comes in
async def chat(request: Request, chat_request: ChatRequest):
    # TODO: Implement AI Integration
    product_list = await fetch_products()
    # 2️Convert to JSON string for Gemini prompt (LLM needs text, not Python objects)
    product_json = json.dumps(product_list, indent=4)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction= f"""
                You are a shopping assistant.
                Here is the product catalog in JSON format: {product_json}.
                Based on the user input: {chat_request.prompt}, 
                pick up to 5 relevant products for the user. 
                Always search the product catalog to find options that fit their request.
                Return your answer in JSON format.
                Always return a JSON object with this structure:  

                {{
                  "answer": "string - natural language explanation to the user",
                  "products": [
                    {{
                      "title": "string - product name",
                      "price": "float - product price",
                      "thumbnail": "string - product image URL",
                      "url": "string - product page URL"
                    }}
                  ]
                }}
                If you can't find any products that match the prompt, 
                direct them to contact support via WhatsApp or instagram messenger.
                Do not use markdown or code fences (```). Only output valid JSON.
                """
        ),
        contents= chat_request.prompt
    )
    try:
        p_data = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        return ChatResponse(answer="Sorry, something went wrong. Please try again.", products=[])

    # Ensure products key exists
    if "products" not in p_data:
        p_data["products"] = []

    return ChatResponse(**p_data)






