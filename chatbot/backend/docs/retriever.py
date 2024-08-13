from langchain_chroma import Chroma
from docs.utils import embedding_function
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from sentence_transformers import CrossEncoder
from langchain.schema import Document
import os


def context_retriever(query):
    persist_directory = os.path.join(
        os.path.dirname(__file__), os.pardir, 'db')
    vector_store = Chroma(persist_directory=persist_directory,
                          embedding_function=embedding_function)

    # Get documents from vector store
    vector_docs = vector_store.get()

    # Create Document objects
    documents = [Document(page_content=text, metadata={})
                 for text in vector_docs['documents']]

    # Create BM25 retriever
    bm25_retriever = BM25Retriever.from_documents(documents)

    # Create semantic retriever
    semantic_retriever = vector_store.as_retriever(search_kwargs={"k": 25})

    # Create hybrid retriever
    hybrid_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, semantic_retriever],
        weights=[0.5, 0.5]
    )

    # Retrieve documents using hybrid search
    docs = hybrid_retriever.get_relevant_documents(query)

    # Re-rank documents
    reranked_docs = rerank_documents(query, docs)

    # Format to form context
    context = "\n\n".join([doc.page_content for doc in reranked_docs])
    return context


def rerank_documents(query, docs, top_k=5):
    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    pairs = [[query, doc.page_content] for doc in docs]
    scores = cross_encoder.predict(pairs)

    ranked_results = sorted(
        zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in ranked_results[:top_k]]
