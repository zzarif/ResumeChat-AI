from langchain_community.vectorstores import Chroma
from docs.utils import embedding


def context_retriever():
    vector_store = Chroma(persist_directory="db", embedding_function=embedding)

    return vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 20,
            "score_threshold": 0.1,
        },
    )
