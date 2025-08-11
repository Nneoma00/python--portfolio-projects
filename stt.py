#STREAMLIT LOGIC
import streamlit as st
import asyncio
import tempfile
import json

# Ensure event loop exists for Streamlit's ScriptRunner thread
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from main import load_file
from test import split_embed, store_vectors, gen_summary, get_response



# st.title("MeetQuery")
# st.caption("Your meetings decoded...")
# st.caption("Upload a transcript. Get instant summaries, action items, and AI-powered answers.")
if "uploaded" not in st.session_state:
    st.session_state["uploaded"] = False


st.markdown(
    "<h1 style='text-align: center;'>MeetQuery</h1>", 
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align: center; color: #444;'>Your meetings, decoded</h3>", 
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: #444; font-size: 18px; margin-top: 0;'>"
    "Upload a transcript. Get instant summaries, action items, and answers to meeting-related questions."
    "</p>",
    unsafe_allow_html=True
)

st.sidebar.header("📄 Upload Meeting Transcript")
# File uploader only shows if no upload yet
if not st.session_state["uploaded"]:
    uploaded_file = st.sidebar.file_uploader(label="Upload text file", type=["pdf", "txt", "vtt"])
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name  # <- This is the file path for LangChain
            #TODO: your file processing logic here
        
        with st.spinner("Processing transcript..."):
            docs = list(load_file(temp_path))  # Pass temp file path to LangChain logic
            embeddings, chunks = split_embed(docs)
            store_vectors(chunks)

        st.session_state["uploaded"] = True
        st.success("File uploaded successfully!")

        summary = gen_summary(docs)  
        st.header("Meeting Summary")
        #st.markdown(summary)
        st.code(summary, language="text")

else:
    st.info("You have already uploaded a file this session.")




    # import os
    # st.write("Temp file exists:", os.path.exists(temp_path))
    # st.write("Temp file size:", os.path.getsize(temp_path))


    

    


#The chat area

# Initialize the uploaded flag

# Initialize chat messages history
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# Chat input box
st.sidebar.warning("⚠ Please limit your questions to **2 per session**.")

query = st.chat_input("Ask a question about the meeting")
if query:
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": query})

    # Show assistant processing message
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Processing...")

        # Call your function to get the response (replace get_response with your actual function)
        answer = get_response(query)

        # Update message bubble with answer
        placeholder.markdown(answer)

    # Save assistant response
    st.session_state["messages"].append({"role": "assistant", "content": answer})

# Render previous chat messages
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).markdown(msg["content"])

# query = st.chat_input("Ask a question about the meeting")
# if query:
#     # Step 2: When user types something, call your function
#     if query:  # ensures it's not empty
#         answer = get_response(query)
#         st.write(answer)
