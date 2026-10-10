from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "rag-async-queue"
PDF_PATH = Path(__file__).parent / "data" / "Learning_Python.pdf"


def is_already_embedded(client: QdrantClient, collection_name: str) -> bool:
    """Check if the collection exists and already has vectors in it."""
    try:
        if not client.collection_exists(collection_name):
            return False
        info = client.get_collection(collection_name)
        return info.points_count is not None and info.points_count > 0
    except Exception as e:
        print(f"Error checking collection status: {e}")
        return False


def run_ingestion():
    """Load, split, embed and store the PDF into Qdrant. Idempotent."""
    client = QdrantClient(url=QDRANT_URL)

    if is_already_embedded(client, COLLECTION_NAME):
        print(f"Collection '{COLLECTION_NAME}' already embedded — skipping ingestion.")
        return

    print(f"Collection '{COLLECTION_NAME}' not found or empty — running ingestion...")

    loader = PyPDFLoader(file_path=str(PDF_PATH))
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=400,
    )
    chunks = text_splitter.split_documents(documents=docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")  # fixed typo

    QdrantVectorStore.from_documents(
        chunks,
        embeddings,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME,
    )

    print(f"PDF data successfully embedded into '{COLLECTION_NAME}'.")