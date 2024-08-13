import streamlit as st
import requests
import sseclient
from helper import (
    validate_files,
    format_response
)

# st.set_page_config(layout="wide")

st.title("ResumeChat AI")

st.markdown("""
    <style>
        .blinking-cursor {
            animation: blink 1s step-end infinite;
        }
        @keyframes blink {
            50% { opacity: 0; }
        }
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []


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
                    with requests.post("http://localhost:8000/upload", files=files_to_upload) as response:
                        response.raise_for_status()

                        result = response.json()
                        if result["status"] == "success":
                            if result["conversion_status"]:
                                st.sidebar.success(
                                    "Context retrieved successfully.")
                            else:
                                st.sidebar.error(
                                    "Error occurred during vector conversion.")
                        else:
                            st.sidebar.error(f"Error uploading files: {
                                            result['message']}")

                except requests.RequestException as e:
                    st.sidebar.error(
                        f"Error communicating with the server: {str(e)}")


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
                with requests.post("http://localhost:8000/chat", json={"query": prompt}, stream=True) as response:
                    if response.status_code == 200:
                        client = sseclient.SSEClient(response)
                        for event in client.events():
                            chunk = event.data.replace('\\n', '\n')
                            full_response += chunk

                            # Format the response with cursor
                            formatted_response = format_response(
                                full_response, include_cursor=True)

                            message_placeholder.markdown(
                                formatted_response, unsafe_allow_html=True)
                    else:
                        st.error(
                            f"Error: {response.status_code} - {response.text}")
            except requests.RequestException as e:
                st.error(f"Error communicating with the server: {str(e)}")

        # Final update without the cursor
        message_placeholder.markdown(format_response(
            full_response), unsafe_allow_html=True)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
