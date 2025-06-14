from settings import PINECONE_API_KEY
from pinecone import Pinecone
import uuid
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PineconeVectorStore:
    """
    A class to manage Pinecone vector database operations including
    document insertion and similarity search.
    """
    
    def __init__(self, index_name: str, dimension: int = 3071, metric: str = "dotproduct"):
        """
        Initialize the Pinecone vector store connection.
        
        Args:
            index_name (str): Name of the Pinecone index
            dimension (int): Dimension of the vectors (default: 3071 for OpenAI embeddings)
            metric (str): Distance metric for similarity search (default: "dotproduct")
        """
        try:
            self.pc = Pinecone(api_key=PINECONE_API_KEY)
            self.index_name = index_name
            self.dimension = dimension
            self.metric = metric
            
            # Check if index exists, create if not
            self._ensure_index_exists()
            
            # Connect to the index
            self.index = self.pc.Index(self.index_name)
            
            logger.info(f"Successfully connected to Pinecone index: {self.index_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone connection: {str(e)}")
            raise
    
    def _ensure_index_exists(self):
        """
        Ensure the Pinecone index exists, create if it doesn't.
        """
        try:
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                logger.info(f"Creating new Pinecone index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric=self.metric,
                    spec={
                        "serverless": {
                            "cloud": "aws",
                            "region": "us-east-1"
                        }
                    }
                )
                logger.info(f"Index {self.index_name} created successfully")
            else:
                logger.info(f"Index {self.index_name} already exists")
                
        except Exception as e:
            logger.error(f"Error ensuring index exists: {str(e)}")
            raise
    
    def add_documents(self, documents: List[Dict[str, Any]], vectors: List[List[float]], 
                     namespace: str = "") -> bool:
        """
        Add documents with their vector embeddings to the Pinecone index.
        
        Args:
            documents (List[Dict]): List of document metadata
            vectors (List[List[float]]): List of vector embeddings for each document
            namespace (str): Namespace to store documents in (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if len(documents) != len(vectors):
                raise ValueError("Number of documents must match number of vectors")
            
            # Prepare vectors for upsert
            vectors_to_upsert = []
            for i, (doc, vector) in enumerate(zip(documents, vectors)):
                # Generate unique ID if not provided
                doc_id = doc.get('id', str(uuid.uuid4()))
                
                vectors_to_upsert.append({
                    'id': doc_id,
                    'values': vector,
                    'metadata': doc
                })
            
            # Upsert vectors in batches
            batch_size = 100
            for i in range(0, len(vectors_to_upsert), batch_size):
                batch = vectors_to_upsert[i:i + batch_size]
                self.index.upsert(vectors=batch, namespace=namespace)
                logger.info(f"Upserted batch {i//batch_size + 1}/{(len(vectors_to_upsert)-1)//batch_size + 1}")
            
            logger.info(f"Successfully added {len(documents)} documents to index {self.index_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents to Pinecone: {str(e)}")
            return False
    
    def add_single_document(self, document: Dict[str, Any], vector: List[float], 
                           namespace: str = "") -> bool:
        """
        Add a single document with its vector embedding to the Pinecone index.
        
        Args:
            document (Dict): Document metadata
            vector (List[float]): Vector embedding for the document
            namespace (str): Namespace to store document in (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.add_documents([document], [vector], namespace)
    
    def similarity_search(self, query_vector: List[float], top_k: int = 10, 
                         namespace: str = "", filter_dict: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Search for similar documents based on vector similarity.
        
        Args:
            query_vector (List[float]): Query vector for similarity search
            top_k (int): Number of top similar documents to return
            namespace (str): Namespace to search in (optional)
            filter_dict (Dict): Metadata filters to apply (optional)
            
        Returns:
            List[Dict]: List of similar documents with scores and metadata
        """
        try:
            query_response = self.index.query(
                vector=query_vector,
                top_k=top_k,
                include_metadata=True,
                include_values=False,
                namespace=namespace,
                filter=filter_dict
            )
            
            results = []
            for match in query_response.matches:
                results.append({
                    'id': match.id,
                    'score': match.score,
                    'metadata': match.metadata
                })
            
            logger.info(f"Found {len(results)} similar documents")
            return results
            
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            return []
    
    def delete_documents(self, document_ids: List[str], namespace: str = "") -> bool:
        """
        Delete documents from the Pinecone index.
        
        Args:
            document_ids (List[str]): List of document IDs to delete
            namespace (str): Namespace to delete from (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.index.delete(ids=document_ids, namespace=namespace)
            logger.info(f"Successfully deleted {len(document_ids)} documents")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting documents: {str(e)}")
            return False
    
    def get_index_stats(self, namespace: str = "") -> Dict[str, Any]:
        """
        Get statistics about the Pinecone index.
        
        Args:
            namespace (str): Namespace to get stats for (optional)
            
        Returns:
            Dict: Index statistics
        """
        try:
            stats = self.index.describe_index_stats()
            
            if namespace:
                namespace_stats = stats.namespaces.get(namespace, {})
                return {
                    'total_vector_count': namespace_stats.get('vector_count', 0),
                    'namespace': namespace
                }
            else:
                return {
                    'total_vector_count': stats.total_vector_count,
                    'dimension': stats.dimension,
                    'index_fullness': stats.index_fullness,
                    'namespaces': dict(stats.namespaces) if stats.namespaces else {}
                }
                
        except Exception as e:
            logger.error(f"Error getting index stats: {str(e)}")
            return {}
    
    def clear_namespace(self, namespace: str) -> bool:
        """
        Clear all vectors from a specific namespace.
        
        Args:
            namespace (str): Namespace to clear
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.index.delete(delete_all=True, namespace=namespace)
            logger.info(f"Successfully cleared namespace: {namespace}")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing namespace {namespace}: {str(e)}")
            return False
