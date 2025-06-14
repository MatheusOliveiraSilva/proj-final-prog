import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# Add backend directory to path for imports
backend_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(backend_dir))

from vector_store.pinecone_utils import PineconeVectorStore
from utils.embeddings import get_openai_embedding
from settings import PINECONE_INDEX_NAME, PINECONE_DIMENSION

# Configure logging
logger = logging.getLogger(__name__)

class DocumentSearch:
    def __init__(self):
        self._vector_store = None
        self.thread_id: Optional[str] = None

    def _get_vector_store(self) -> PineconeVectorStore:
        """Get or create vector store instance"""
        if self._vector_store is None:
            self._vector_store = PineconeVectorStore(
                index_name=PINECONE_INDEX_NAME,
                dimension=PINECONE_DIMENSION
            )
        return self._vector_store

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
    # Test the class with different namespace scenarios
    doc_search = DocumentSearch()
    query = "What is machine learning?"
    
    print("=== Search in all namespaces ===")
    results = doc_search.search(query, top_k=3)
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc['title']}")
        print(f"   Score: {doc['score']:.3f}")
        print(f"   Chunk: {doc['chunk_index'] + 1}/{doc['total_chunks']} ({doc['chunk_size']} chars)")
        print(f"   Content: {doc['content'][:100]}...")
        print(f"   Source: {doc['source']}")
        print(f"   Document ID: {doc['original_document_id']}")
        print("-" * 50)
    
    print("\n=== Search in specific namespace ===")
    doc_search.thread_id = "thread_s-49308-91bk88-8f227c9e"
    results_filtered = doc_search.search(query, top_k=3)

    for i, doc in enumerate(results_filtered, 1):
        print(f"{i}. {doc['title']}")
        print(f"   Score: {doc['score']:.3f}")
        print(f"   Chunk: {doc['chunk_index'] + 1}/{doc['total_chunks']} ({doc['chunk_size']} chars)")
        print(f"   Content: {doc['content'][:100]}...")
        print(f"   Source: {doc['source']}")
        print(f"   Document ID: {doc['original_document_id']}")
        print("-" * 50)
