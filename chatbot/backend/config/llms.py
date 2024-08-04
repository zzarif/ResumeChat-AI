from langchain_community.chat_models import ChatOllama
from langchain_core.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llama3 = ChatOllama(
    base_url='http://localhost:11434',
    model="llama3",
    temperature=0,
    streaming=True,
    callback_manager=callback_manager
)


mistral = ChatOllama(
    base_url='http://localhost:11434',
    model="mistral",
    temperature=0,
    streaming=True,
    callback_manager=callback_manager
)


llama2_uncensored = ChatOllama(
    base_url='http://localhost:11434',
    model="llama2-uncensored",
    temperature=0,
    streaming=True,
    callback_manager=callback_manager
)