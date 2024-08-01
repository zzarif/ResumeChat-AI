from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from docs.retriever import context_retriever
from chatbot.utils import llm, prompt_template
from typing import AsyncIterable


async def stream_response(query: str) -> AsyncIterable[str]:
    rag_chain = (
        {"context": context_retriever(), "question": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )

    async for chunk in rag_chain.astream(query):
        yield chunk
