from langchain.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document
import os

# Define path for storing vector embeddings
VECTOR_STORE_PATH = "results/vector_stores/"

# Initialize the embedding model - MiniLM is a lightweight but effective model for text embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def create_vector_store(chunks, filename):
    """
    Create and save a FAISS vector store from text chunks.
    
    Args:
        chunks: List of dictionaries containing content and metadata
        filename: Name of the file to save the vector store
        
    Returns:
        FAISS vector store object
    """
    # Convert chunks to LangChain Document objects with metadata
    documents = [
        Document(
            page_content=chunk["content"],
            metadata={
                "country_codes": chunk["country_codes"],
                "published_date": chunk["published_date"]
            }
        ) for chunk in chunks
    ]

    # Verify all documents have required metadata
    assert all("country_codes" in doc.metadata and 
           "published_date" in doc.metadata 
           for doc in documents), "All documents must have country_codes and published_date metadata"
    
    # Extract text content from documents
    texts = [doc.page_content for doc in documents]
    
    # Generate embeddings for all texts at once (more efficient than one by one)
    embeddings = embedding_model.encode(texts)

    # Create FAISS vector store with text-embedding pairs and metadata
    vector_store = FAISS.from_embeddings(
        text_embeddings=list(zip(texts, embeddings)),
        embedding=embedding_model.encode,
        metadatas=[doc.metadata for doc in documents]
    )
    
    # Save vector store to disk for later use
    vector_store.save_local(f"{VECTOR_STORE_PATH}/{filename}")
    return vector_store

def find_similar_chunks(vector_store):
    """
    Find chunks in the vector store relevant to a military casualties query.
    
    Args:
        vector_store: FAISS vector store to search
        
    Returns:
        List of similar documents from the vector store
    """
    # Example query about military casualties
    query = "Find dates and death counts related to military forces killed in combat."
    
    # Return top 10 most similar documents
    return vector_store.similarity_search(query, k=10)

def retrieve_vector_store(filename):
    """
    Retrieve a vector store by filename with proper error handling.
    
    Args:
        filename: Name of the vector store file to load
        
    Returns:
        FAISS vector store object
    
    Raises:
        FileNotFoundError: If vector store file doesn't exist
        Exception: For other loading errors
    """
    filepath = f"{VECTOR_STORE_PATH}/{filename}"
    
    # Check if file exists before attempting to load
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Vector store not found at {filepath}")
    
    try:
        # Define a flexible embedding function that handles different input types
        def embedding_function(text):
            if isinstance(text, dict):
                # Extract text from dictionary
                return embedding_model.encode(text.get("text", ""))
            elif isinstance(text, str):
                # Process string directly
                return embedding_model.encode(text)
            elif isinstance(text, list):
                # Process list (potentially of strings)
                return embedding_model.encode(text)
            else:
                # Convert any other type to string
                return embedding_model.encode(str(text))
        
        # Load vector store with the flexible embedding function
        return FAISS.load_local(filepath, embedding_function)
    except Exception as e:
        print(f"Error loading vector store: {e}")
        raise
