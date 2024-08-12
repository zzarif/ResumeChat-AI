from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from docs.retriever import context_retriever
from config.prompts import (
    chat_prompt_template,
    ext_prompt_template,
)
from config.llms import llama3
from typing import AsyncIterable


# generate streamed response for chatbot
async def stream_response(query: str) -> AsyncIterable[str]:

    # retrieve context from query
    context = context_retriever(query)

    # from rag chain
    rag_chain = (
        {"context": lambda x: context, "question": RunnablePassthrough()}
        | chat_prompt_template
        | llama3
        | StrOutputParser()
    )

    async for chunk in rag_chain.astream(query):
        encoded_chunk = chunk.replace('\n', '\\n')
        yield f"data: {encoded_chunk}\n\n"


# generate non-streamed response for extension
async def extension_response(context: str, query: str) -> str:

    # from rag chain
    rag_chain = (
        {"context": lambda x: context, "question": RunnablePassthrough()}
        | ext_prompt_template
        | llama3
        | StrOutputParser()
    )

    return rag_chain.invoke(query).strip('"')
