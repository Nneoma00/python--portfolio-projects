# Welcome To My Python Projects!

This repository contains Python scripts and applications, for backend services and AI-powered systems.
My projects touch on:
- API Development & Backend Services (FastAPI, Django)
- Data mining & data analysis (pandas, numpy, JSON)
- AI integration (Gemini, OpenAI API, HuggingFace, LiteLLM, LangChain)
- UI for demos: Streamlit, CodePen, (basic) HTML, CSS, JS

## Projects:

### 1. [**FastAPI e-Commrerce Chatbot**:](https://github.com/Nneoma00/python--portfolio-projects/tree/main/woo-chatbot)
Inspired by a recent client project, I built this fun FastAPI application, featuring an AI "chat" endpoint. Suitable for e-commerce sites—particularly WooCommerce/WordPress.
**Stack Overview:** Python, FastAPI, Gemini, SlowAPI, Pytest, HTTPX, JSON, Pydantic 

𝗣𝗿𝗼𝗷𝗲𝗰𝘁 𝗛𝗶𝗴𝗵𝗹𝗶𝗴𝗵𝘁𝘀: 

1️⃣ Defined `ChatRequest` and `ChatResponse` Pydantic models to handle structured request/response schemas — enabling automatic validation and JSON serialization for the chatbot API.
Implemented rate limiting and proper 429 error handling — with slowapi.

2️⃣ Designed the AI system instruction to return structured JSON output, making it easier for the frontend to parse, display, or loop over responses.

3️⃣ Wrote a pytest suite to validate API behavior.

4️⃣ Deployed the API on Render, with auto-redeployment connected to GitHub pushes so every code update reflects instantly.

### 2. [**meetQuery: RAG app for uploading meeting transcripts**](https://github.com/Nneoma00/python--portfolio-projects/tree/b0d7593daff370a84618b25300fa17a4be978ea6/meetQuery)

MeetQuery is a RAG app that ingests meeting transcripts (PDF, TXT, VTT), generates instant summaries, and lets users chat with the content interactively.

Built with LangChain + Gemini, Pinecone, and Streamlit. Try it here: [meetquery.streamlit.app](https://meetquery.streamlit.app/)

### 3. [**Inventory Microservice API : FastAPI + Redis**](https://github.com/Nneoma00/python--portfolio-projects/tree/b0d7593daff370a84618b25300fa17a4be978ea6/inventory-microservice)
This project is a CRUD-based inventory microservice API built using FastAPI. It allows users to create, read, update, and delete inventory items efficiently. 
The service connects to a Redis Cloud database using redis-om, enabling fast and scalable data storage.

**Tech Stack** : Python, FastAPI, Redis-OM, Uvicorn

  
4. 
