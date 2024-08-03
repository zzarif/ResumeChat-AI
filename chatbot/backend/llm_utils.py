from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_community.chat_models import ChatOllama
from langchain_core.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


review_template_str = """
You are an assistant for question-answering tasks. Use the following 
pieces of retrieved context to answer the question. If you don't know 
the answer, just say that you don't know. Use three sentences maximum 
and keep the answer concise.

{context}
"""

system_message = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["context"], template=review_template_str)
)

user_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["question"], template="{question}")
)
messages = [system_message, user_prompt]

prompt_template = ChatPromptTemplate(
    input_variables=["context", "question"], messages=messages
)


callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = ChatOllama(
    base_url='http://localhost:11434',
    model="llama3",
    temperature=0,
    streaming=True,
    callback_manager=callback_manager
)
