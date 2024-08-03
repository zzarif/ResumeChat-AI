from langchain_chroma import Chroma
from docs.utils import embedding
import os


def context_retriever(query):
    persist_directory = os.path.join(
        os.path.dirname(__file__), os.pardir, 'db')

    vector_store = Chroma(persist_directory=persist_directory,
                          embedding_function=embedding)

    # semantic search for query
    docs_chroma = vector_store.similarity_search_with_score(query=query, k=5)

    # format to form context
    context = "\n\n".join([doc.page_content for doc, _score in docs_chroma])
    return context
