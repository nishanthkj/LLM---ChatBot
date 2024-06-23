from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

# Path to the directory containing PDF files
DATA_PATH = "../Data/PDF"
# Path to save the FAISS vector store
DB_FAISS_PATH = "../Data/vectorstores/db_faiss"

def create_vector_db():
    # Verify the directory exists
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Directory not found: '{DATA_PATH}'")
    
    # Load PDF documents from the specified directory
    loader = DirectoryLoader(DATA_PATH, glob='*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()

    # Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=500)
    texts = text_splitter.split_documents(documents)

    # Generate embeddings using the specified model
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    # Create and save the FAISS vector store
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)

if __name__ == '__main__':
    create_vector_db()
