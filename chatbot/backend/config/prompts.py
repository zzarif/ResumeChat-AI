from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

#################################### CHATBOT PROMPTS #########################################

cb_template_str = """
You are an assistant for question-answering tasks. Use the following 
pieces of retrieved context to answer the question. If you don't know 
the answer, just say that you don't know. Use three sentences maximum 
and keep the answer concise.

{context}
"""

cb_system_message = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["context"], template=cb_template_str)
)

cb_user_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["question"], template="{question}")
)

cb_messages = [cb_system_message, cb_user_prompt]

chat_prompt_template = ChatPromptTemplate(
    input_variables=["context", "question"], messages=cb_messages
)

#################################### EXTENSION PROMPTS #########################################

ext_template_str = """
You're an expert in your field who's experienced in creating engagement on LinkedIn.
Your goal is to maximize engagement between you, the original poster, and other people 
engaging with the post. You'll be provided with the name of the poster, the content 
of the post itself and the intended emotion for the response.

{context}
"""

ext_system_message = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["context"], template=ext_template_str)
)

ext_user_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["question"], template="{question}")
)

ext_messages = [ext_system_message, ext_user_prompt]

ext_prompt_template = ChatPromptTemplate(
    input_variables=["context", "question"], messages=ext_messages
)
