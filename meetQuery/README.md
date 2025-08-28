
# About MeetQuery  

MeetQuery is a **RAG app** that ingests meeting transcripts (PDF, TXT, VTT), generates summaries, and lets users chat with the content interactively.  

Built with [LangChain](https://www.langchain.com/) + [Gemini](https://ai.google/), [Pinecone](https://www.pinecone.io/), and [Streamlit](https://streamlit.io/). 


![MeetQuery UI](https://raw.githubusercontent.com/Nneoma00/python--portfolio-projects/main/demos/meetquery-ui.JPG)


## 🎥 Demo
[Watch a Quick Demo](https://www.youtube.com/watch?v=H2H9VQeocCshttps://youtu.be/H2H9VQeocCs)


[![Watch the demo](https://img.youtube.com/vi/H2H9VQeocCs/0.jpg)](https://www.youtube.com/watch?v=H2H9VQeocCs)


## Features
- Upload transcripts in **PDF, TXT, or VTT** format  
- Generate concise **summaries**  
- Ask questions and chat with your files (limited to **2 questions per session** under free plan)  


## 💻 Tech Stack
- **LangChain** – orchestration  
- **Gemini** – LLM  
- **Pinecone** – vector storage & semantic search  
- **Streamlit** – front end  


## 🚀 Getting Started

1. Clone the repo:  
   ```bash
   git clone https://github.com/Nneoma00/python--portfolio-projects/meetQuery.git
   cd MeetQuery
    ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Add your API keys (Gemini + Pinecone) in a `.env` file:

   ```
   GEMINI_API_KEY=your_key_here
   PINECONE_API_KEY=your_key_here
   ```

4. Run the app:

   ```bash
   streamlit run app.py
   ```

## 🌐 Try It

A hosted demo is available here 👉 [Try MeetQuery](https://meetquery.streamlit.app/)

## 📜 License

MIT

