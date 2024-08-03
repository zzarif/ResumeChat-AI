<h1 align="center">
  <br>
  <!-- <a href="http://www.amitmerchant.com/electron-markdownify"><img src="https://raw.githubusercontent.com/amitmerchant1990/electron-markdownify/master/app/img/markdownify.png" alt="Markdownify" width="200"></a>
  <br> -->
  Llama Resume Chatbot (🛠️ Under Construction)
  <br>
</h1>

<h4 align="center">A RAG chatbot to chat with Resume and extension to connect on LinkedIn</h4>

<p align="center">
  <!-- <a href="https://badge.fury.io/js/electron-markdownify">
    <img src="https://badge.fury.io/js/electron-markdownify.svg"
         alt="Gitter">
  </a>
  <a href="https://gitter.im/amitmerchant1990/electron-markdownify"><img src="https://badges.gitter.im/amitmerchant1990/electron-markdownify.svg"></a>-->
  <!-- <a href="">
      <img src="https://img.shields.io/badge/website-online-blue.svg">
  </a>
  <a href="">
    <img src="https://img.shields.io/badge/dataset-released-green.svg">
  </a>  -->
<a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/license-MIT-yellow.svg">
  </a>

</p>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-chatbot">Chatbot</a> •
  <a href="#-chrome-extension">Chrome Extension</a> •
  <a href="#-build-from-source">Build from Source</a> •
  <a href="#-contact">Contact</a>
</p>

## 📋 Overview

A Retrieval-Augmented Generation app to chat with Resume and Chrome Extension to connect on LinkedIn. Key features:
- Utilizes open-source embedding model to retrieve context by converting large PDF documents into vector databases.
- Implements **FastAPI** backend that utilizes **LangChain** to invoke open-source LLMs and produce streamed response.
- Developed an interactive chatbot with **Streamlit** that uses **SSEClient** to handle streams.

## 🧠 Architecture

![RAG Architecture](https://miro.medium.com/v2/resize:fit:4800/format:webp/1*H1AT2nqq-MAf-6vz62TemQ.png)

<p align="center">Image Source: <a href="https://medium.com/@vectorizeio/which-is-the-best-vector-database-for-rag-applications-e559822aeccd">Medium</a></p>

## 💬 Chatbot

## 🌐 Chrome Extension

## ⚙️ Build from Source

### Serve Ollama

1. Download and install **Ollama** from https://ollama.com/download

2. Pull required open-source LLMs (here we use [`llama3`](https://ollama.com/library/llama3), you can use other models like [`mistral`](https://ollama.com/library/mistral), [`llama2-uncensored`](https://ollama.com/library/llama2-uncensored), etc.)

```bash
ollama pull llama3
```

3. Pull required embedding models (here we use [`nomic-embed-text`](https://ollama.com/library/nomic-embed-text))

```bash
ollama pull nomic-embed-text
```

4. Serve Ollama locally (by default Ollama is served from `http://localhost:11434`)

```bash
ollama serve
```

Note: If this command results in an error, make sure to quit any running Ollama background processes.

### Setup Server and Chatbot

1. Clone the repository

```bash
git clone https://github.com/zzarif/Llama-Resume-Chatbot.git
cd Llama-Resume-Chatbot/
```

2. Install necessary dependencies

```bash
poetry install
```

3. Activate virtual environment

```bash
poetry shell
```

4. Start chatbot backend server (served from `http://localhost:8000`)

```bash
python chatbot/backend/api.py
```

5. Launch the chatbot (served from `http://localhost:8501`)

```bash
streamlit run chatbot/main.py
```

## 🌐 Contact:

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/zibran-zarif-amio-b82717263/) [![Mail](https://img.shields.io/badge/Gmail-EA4335?logo=gmail&logoColor=fff)](mailto:zibran.zarif.amio@gmail.com)
