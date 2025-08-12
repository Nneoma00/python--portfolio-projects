from langchain_community.document_loaders import PyPDFLoader
import os
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = st.secrets("GOOGLE_API_KEY")

ENDPOINT =os.getenv("ENDPOINT")
PINECONE_KEY = st.secrets("PINECONE_KEY")

#SELECT CHAT MODEL
from langchain.chat_models import init_chat_model
llm = init_chat_model("gemini-2.5-flash", model_provider="google-genai")

#SELECT EMBEDDINGS MODEL
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

#SELECT VECTOR STORE
pc = Pinecone(api_key=PINECONE_KEY)
index = pc.Index("lang-demo")
vector_store = PineconeVectorStore(embedding=embeddings_model, index=index)

#LOAD UPLOADED FILES INTO A DOCUMENT OBJECT
def load_file():
    loader = PyPDFLoader("meetingz.pdf")
    docs = loader.lazy_load()
    return docs
#This is a static function...only works with the meetingz.pdf file.

#Split file into document objects and embed
def split_embed(docs):

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
    texts = [chunk.page_content for chunk in chunks]    
    embeddings = embeddings_model.embed_documents(texts)
    return embeddings, chunks


def store_vectors(chunks):
    document_ids = vector_store.add_documents(documents=chunks)
    return document_ids

def gen_summary(docs):
    if not docs:
        return "No content found in the document."
    
    meeting_text = " ".join([doc.page_content for doc in docs]) 
    prompt = f"""
    Summarize the following meeting transcript. 
    List key action items, their due date and responsible persons only if indicated.
    Ignore the timestamps and focus on meeting content.

    Transcript:
    {meeting_text}
    """
    response = llm.invoke(prompt)
    return response.content


def get_response(query):

    similar_docs = vector_store.similarity_search(query, k=5)
    if not similar_docs:
        return "I couldn't find any relevant context"
    
    context = "\n\n".join(doc.page_content for doc in similar_docs)
    system_prompt = """You are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer the question. Names indicate meeting participants.
    Keep answers concise, 3 sentences maximum.
    Context: {context}:"""

    system_prompt_format = system_prompt.format(context=context)
    response = llm.invoke([SystemMessage(content=system_prompt_format),
                            HumanMessage(content=query)])
    return response.content.strip()



# Optional: local testing only
if __name__ == "__main__":
    docs = load_file()
    embeddings, chunks = split_embed(docs)
    store_vectors(chunks)
    gen_summary(docs)
    query = input("Ask a question about the meeting: ")
    print(get_response(query))

