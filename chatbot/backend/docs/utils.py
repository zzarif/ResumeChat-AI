from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
# model_name = "sentence-transformers/all-mpnet-base-v2"

# Create the embedding function
embedding_function = HuggingFaceEmbeddings(model_name=embedding_model)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024,
    chunk_overlap=80,
    length_function=len,
    separators=["\n\n", "\n", ".", " ", ""]
)
