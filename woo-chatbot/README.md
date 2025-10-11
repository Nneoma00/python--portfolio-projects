# **eCommerce REST API**

This project is an AI-powered Sales Chatbot for an eCommerce marketplace. 

The backend service (**FastAPI**) interfaces with an AI model (**Gemini**), to deliver real-time product recommendations tailored to user search prompts.

Fully compatible with WooCommerce/WordPress workflows, with an embeddable script for the frontend. 
The _chat_ endpoint handles queries about products, and redirects users to alternative channels if an answer isn’t available.

This application also includes a custom rate limit handler **(2 requests per minute)**, to handle high traffic gracefully.

## Tech Stack
1. **Backend:** Python, FastAPI, httpx AsyncClient, Slowapi, requests, JSON, pytest
2. **Frontend:** HTML, CSS, JavaScript (test on CodePen or localhost)
3. **AI Integration:** Gemini 2.5 pro
4. **Deployment:** Render (backend), CodePen (frontend)


## Try it!
* **Interact with the UI:** https://codepen.io/Nneoma-Uche/full/azdpmQB
* **Live API on Render:** https://ecommerce-chatbot-api.onrender.com/
* **Try the docs!:** https://ecommerce-chatbot-api.onrender.com/docs


## How to Use
1. Open the **frontend CodePen link**.  
2. Type your query about a product in the input box.  
3. Submit your query:  
   * If the AI finds the product(s) in stock, it outputs a response, along with product recommendations, immediately.  
   * If the AI can’t answer, you’ll be redirected to the appropriate channel for further assistance.  
4. The system is **rate-limited**, so repeated requests may temporarily return a “Too Many Requests” message.


## **Code & Setup (for developers)**

1. **Clone the repository:**  
```
# Clone only the woo-chatbot folder (advanced users)
git clone --no-checkout https://github.com/Nneoma00/python--portfolio-projects.git
cd python--portfolio-projects
git sparse-checkout init --cone
git sparse-checkout set woo-chatbot
```

2. **Install dependencies:**  
`pip install -r requirements.txt`

3.  **Set environment variables:**  
`GEMINI_API_KEY=your_api_key`

3. **Run the FastAPI backend locally (optional):**  
`uvicorn main:app --reload`

4.**Frontend:** Update the API URL in `index.html` to point to your deployed backend if testing locally.



## **Screenshots / Demo**

![Sample chat UI](woo-chatbot/demo-imgs/orange-chatbot.JPG)

![Rate Limit Error on Localhost](woo-chatbot/demo-imgs/rate-limit.JPG)


---

## **License**

MIT License
