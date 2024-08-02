# Llama Resume Chat (Under construction)

RAG Chatbot to chat and connect with your resume

## Download and Install Ollama
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

## Build from Source
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

