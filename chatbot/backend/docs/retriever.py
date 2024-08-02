from langchain_community.vectorstores import Chroma
from docs.utils import embedding
import os


def context_retriever():
    persist_directory = os.path.join(
        os.path.dirname(__file__), os.pardir, 'db')

    vector_store = Chroma(persist_directory=persist_directory,
                          embedding_function=embedding)

    return vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 20,
            "score_threshold": 0.1,
        },
    )
