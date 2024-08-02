from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_community.chat_models import ChatOllama
from langchain_core.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


review_template_str = """Your job is to use a person's Resume to answer 
questions about their skills and experiences. Use the following context to 
answer questions. Be as detailed as possible, but don't make up any information 
that's not from the context. If you don't know an answer, say you don't know.

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
    model="llama2-uncensored",
    temperature=0,
    streaming=True,
    callback_manager=callback_manager
)
