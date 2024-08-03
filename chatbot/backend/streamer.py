from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from docs.retriever import context_retriever
from llm_utils import llm, prompt_template
from typing import AsyncIterable


async def stream_response(query: str) -> AsyncIterable[str]:

    # retrieve context from query
    context = context_retriever(query)

    # from rag chain
    rag_chain = (
        {"context": lambda x: context, "question": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )

    async for chunk in rag_chain.astream(query):
        yield f"data: {chunk}\n\n"
