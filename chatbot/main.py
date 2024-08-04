import streamlit as st
import requests
import sseclient

# st.set_page_config(layout="wide")

st.title("Llama Resume Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

def validate_files(uploaded_files):
    invalid_files = []
    for file in uploaded_files:
        if file.type != "application/pdf":
            invalid_files.append((file.name, "Not a PDF file"))
        elif file.size > 20 * 1024 * 1024:  # 20MB in bytes
            invalid_files.append((file.name, "Exceeds 20MB limit"))
    return invalid_files

# Sidebar for file upload
with st.sidebar:
    st.sidebar.title("PDF File Uploader")

    uploaded_files = st.sidebar.file_uploader(
        "Choose PDF files",
        accept_multiple_files=True,
        type=["pdf"]
    )

    if uploaded_files:
        invalid_files = validate_files(uploaded_files)

        if invalid_files:
            error_message = "The following files are invalid:\n"
            for file, reason in invalid_files:
                error_message += f"- {file}: {reason}\n"
            st.sidebar.error(error_message)
        else:
            files_to_upload = [("files", file) for file in uploaded_files]
            
            with st.spinner('Retrieving context... Please wait.'):
                try:
                    response = requests.post("http://localhost:8000/upload", files=files_to_upload)
                    response.raise_for_status()
                    
                    result = response.json()
                    if result["status"] == "success":
                        if result["conversion_status"]:
                            st.sidebar.success("Context retrieved successfully.")
                        else:
                            st.sidebar.error("Error occurred during vector conversion.")
                    else:
                        st.sidebar.error(f"Error uploading files: {result['message']}")
                
                except requests.RequestException as e:
                    st.sidebar.error(f"Error communicating with the server: {str(e)}")

# Main chat interface
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

        with st.spinner("Thinking..."):
            try:
                # Send request to FastAPI backend
                with requests.post("http://localhost:8000/chat", json={"query": prompt}, stream=True) as response:
                    if response.status_code == 200:
                        client = sseclient.SSEClient(response)
                        for event in client.events():
                            full_response += event.data
                            message_placeholder.markdown(full_response + "▌")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
            except requests.RequestException as e:
                st.error(f"Error communicating with the server: {str(e)}")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
