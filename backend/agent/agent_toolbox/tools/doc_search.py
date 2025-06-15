import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from langchain_core.tools import tool

# Add backend directory to path for imports
backend_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(backend_dir))

from vector_store.pinecone_utils import PineconeVectorStore
from utils.embeddings import get_openai_embedding
from settings import PINECONE_INDEX_NAME, PINECONE_DIMENSION

# Configure logging
logger = logging.getLogger(__name__)

# Global vector store instance
_vector_store = None

def get_vector_store() -> PineconeVectorStore:
    """Get or create vector store instance"""
    global _vector_store
    if _vector_store is None:
        _vector_store = PineconeVectorStore(
            index_name=PINECONE_INDEX_NAME,
            dimension=PINECONE_DIMENSION
        )
    return _vector_store

@tool
def search_documents(query: str, top_k: int = 10) -> List[Dict[str, Any]]:
    """
    Search for the most relevant documents in the chatwithdocs index.
    
    This function converts the query text to embeddings using OpenAI's text-embedding-3-large
    model and performs similarity search in the Pinecone vector database.
    
    Use this tool when users ask questions about uploaded documents or need information 
    from their document collection.
    
    Args:
        query (str): Search query text
        top_k (int): Number of top results to return (default: 10)
        
    Returns:
        List[Dict[str, Any]]: List of relevant documents with the following structure:
            - document_id (str): Unique document identifier
            - score (float): Similarity score (higher is more relevant)
            - title (str): Document title
            - content (str): Document content
            - source (str): Document source
            - metadata (dict): Full document metadata
    """
    try:
        # Get thread_id from current context (will be injected by the tool executor)
        from langchain_core.callbacks.manager import CallbackManagerForToolRun
        import contextvars
        
        # Try to get thread_id from context
        thread_id = getattr(search_documents, '_current_thread_id', None)
        
        if thread_id:
            logger.info(f"Searching for documents with query: '{query}' in namespace: '{thread_id}' (top_k={top_k})")
        else:
            logger.info(f"Searching for documents with query: '{query}' in all threads (top_k={top_k})")
        
        # Generate embedding for the query
        query_embedding = get_openai_embedding(query)
        
        # Get vector store instance
        vector_store = get_vector_store()
        
        # Perform similarity search with namespace filter
        results = vector_store.similarity_search(
            query_vector=query_embedding,
            top_k=top_k,
            namespace=thread_id
        )
        
        logger.info(f"Found {len(results)} relevant documents")
        
        # Format results for easier consumption
        formatted_results = []
        for result in results:
            # Extract chunk information
            chunk_info = {
                'document_id': result['id'],
                'score': result['score'],
                'title': result['metadata'].get('title', 'Unknown'),
                'content': result['metadata'].get('content', ''),
                'source': result['metadata'].get('source', 'Unknown'),
                'original_document_id': result['metadata'].get('original_document_id', result['id']),
                'chunk_index': result['metadata'].get('chunk_index', 0),
                'total_chunks': result['metadata'].get('total_chunks', 1),
                'chunk_size': result['metadata'].get('chunk_size', len(result['metadata'].get('content', ''))),
                'metadata': result['metadata']
            }
            formatted_results.append(chunk_info)
        
        return formatted_results
        
    except Exception as e:
        logger.error(f"Error searching documents: {str(e)}")
        return []

class DocumentSearch:
    """Legacy class for backward compatibility"""
    def __init__(self, thread_id: Optional[str] = None):
        self._vector_store = None
        self.thread_id = thread_id

    def _get_vector_store(self) -> PineconeVectorStore:
        """Get or create vector store instance"""
        if self._vector_store is None:
            self._vector_store = PineconeVectorStore(
                index_name=PINECONE_INDEX_NAME,
                dimension=PINECONE_DIMENSION
            )
        return self._vector_store

    def set_thread_id(self, thread_id: str) -> None:
        """Set the thread_id for namespace filtering"""
        self.thread_id = thread_id
        logger.info(f"DocumentSearch thread_id set to: {thread_id}")

    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Search for the most relevant documents in the chatwithdocs index.
        
        This function converts the query text to embeddings using OpenAI's text-embedding-3-large
        model and performs similarity search in the Pinecone vector database.
        
        Args:
            query (str): Search query text
            top_k (int): Number of top results to return (default: 10)
            
        Returns:
            List[Dict[str, Any]]: List of relevant documents with the following structure:
                - document_id (str): Unique document identifier
                - score (float): Similarity score (higher is more relevant)
                - title (str): Document title
                - content (str): Document content
                - source (str): Document source
                - metadata (dict): Full document metadata
        """
        try:
            if self.thread_id:
                logger.info(f"Searching for documents with query: '{query}' in namespace: '{self.thread_id}' (top_k={top_k})")
            else:
                logger.info(f"Searching for documents with query: '{query}' in all threads (top_k={top_k})")
            
            # Generate embedding for the query
            query_embedding = get_openai_embedding(query)
            
            # Get vector store instance
            vector_store = self._get_vector_store()
            
            # Perform similarity search with namespace filter
            results = vector_store.similarity_search(
                query_vector=query_embedding,
                top_k=top_k,
                namespace=self.thread_id
            )
            
            logger.info(f"Found {len(results)} relevant documents")
            
            # Format results for easier consumption
            formatted_results = []
            for result in results:
                # Extract chunk information
                chunk_info = {
                    'document_id': result['id'],
                    'score': result['score'],
                    'title': result['metadata'].get('title', 'Unknown'),
                    'content': result['metadata'].get('content', ''),
                    'source': result['metadata'].get('source', 'Unknown'),
                    'original_document_id': result['metadata'].get('original_document_id', result['id']),
                    'chunk_index': result['metadata'].get('chunk_index', 0),
                    'total_chunks': result['metadata'].get('total_chunks', 1),
                    'chunk_size': result['metadata'].get('chunk_size', len(result['metadata'].get('content', ''))),
                    'metadata': result['metadata']
                }
                formatted_results.append(chunk_info)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []


# Example usage
if __name__ == "__main__":
    # Test the function
    query = "What is machine learning?"
    
    print("=== Testing search_documents function ===")
    results = search_documents(query, top_k=3)
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc['title']}")
        print(f"   Score: {doc['score']:.3f}")
        print(f"   Chunk: {doc['chunk_index'] + 1}/{doc['total_chunks']} ({doc['chunk_size']} chars)")
        print(f"   Content: {doc['content'][:100]}...")
        print(f"   Source: {doc['source']}")
        print(f"   Document ID: {doc['original_document_id']}")
        print("-" * 50)
