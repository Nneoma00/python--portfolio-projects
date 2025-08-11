#pip install webvtt-py
import os
from webvtt import WebVTT
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def load_file(file_path):
    #this is where I write the logic to determine if the file extension is pdf, vtt or txt
    #file_path = input("Upload file: ")
    #we'll use os.path.splitext() to find the extension
    root, extension = os.path.splitext(file_path)
    if extension == ".pdf":
        loader = PyPDFLoader(file_path)
        docs = loader.lazy_load()

    # elif extension == ".txt":
    #     loader = TextLoader(file_path, encoding="utf-8")
    #     docs = loader.lazy_load()

    elif extension == ".txt":
        try:
            loader = TextLoader(file_path, encoding="utf-8")
        except UnicodeDecodeError:
            loader = TextLoader(file_path, encoding="latin-1")
        docs = loader.lazy_load()


    elif extension == ".vtt":
        text_content = []
        for caption in WebVTT().read(file_path):
            text_content.append(caption.text)
        vtt_string = "\n".join(text_content)
        docs = Document(page_content=vtt_string, metadata={"source": "cleaned_string"})

    else:
        raise ValueError("Upload a supported file format: 'PDF', 'VTT' or 'TXT'.")
    
    return docs


    


# def split_embed():

#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     chunks = text_splitter.split_documents(docs)
#     #Extract text content for embeddings

#     texts = [chunk.page_content for chunk in chunks]

#     embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
#     embeddings = embeddings_model.embed_documents(texts)
#     return embeddings, chunks
# embeddings, chunks = split_embed()

#check if the text was split in chunks
#print(f"Number of chunks: {len(chunks)}")


if __name__ == "__main__":
    docs = load_file(file_path="meetingz.pdf")