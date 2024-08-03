from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from docs.utils import text_splitter, embedding
import os


def save_doc_to_vector_store(file):
    try:
        # load PDF file
        file_path = os.path.join(os.path.dirname(
            __file__), 'pdfs', file.filename)
        loader = PyPDFLoader(file_path)

        # split pdf into chunks
        docs = loader.load_and_split()
        chunks = text_splitter.split_documents(docs)

        # save to vector store
        persist_directory = os.path.join(
            os.path.dirname(__file__), os.pardir, 'db')
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            persist_directory=persist_directory
        )

        return vector_store

    except Exception as e:
        print(e)
        return None
