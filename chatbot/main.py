import streamlit as st
import requests
import sseclient
import os

st.title("Llama Resume Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# File upload section
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    # Save the file locally
    with open(os.path.join(os.path.dirname(__file__), 'backend', 'docs', 'pdfs', uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Send the file to the FastAPI backend
    files = {"file": (uploaded_file.name,
                      uploaded_file.getvalue(), "application/pdf")}
    upload_response = requests.post(
        "http://localhost:8000/upload", files=files)

    if upload_response.status_code == 200:
        st.success(f"File {uploaded_file.name} uploaded successfully!")
    else:
        st.error("Error uploading file.")

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Send request to FastAPI backend
        with requests.post("http://localhost:8000/chat", json={"query": prompt}, stream=True) as response:
            if response.status_code == 200:
                client = sseclient.SSEClient(response)
                for event in client.events():
                    full_response += event.data
                    message_placeholder.markdown(full_response + "▌")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
