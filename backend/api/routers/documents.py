from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
import logging

from vector_store.pinecone_utils import PineconeVectorStore
from settings import PINECONE_INDEX_NAME, PINECONE_DIMENSION
from api.schemas.document_schemas import (
    UploadDocumentRequest,
    BulkUploadDocumentRequest,
    DeleteDocumentRequest,
    SimilaritySearchRequest,
    DocumentResponse,
    SimilaritySearchResponse,
    IndexStatsResponse
)

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

# Global vector store instance
vector_store: PineconeVectorStore = None

def get_vector_store() -> PineconeVectorStore:
    """Get or create vector store instance"""
    global vector_store
    if vector_store is None:
        vector_store = PineconeVectorStore(
            index_name=PINECONE_INDEX_NAME,
            dimension=PINECONE_DIMENSION
        )
    return vector_store


def clean_metadata(metadata: dict) -> dict:
    """
    Clean metadata by removing None values and ensuring compatibility with Pinecone.
    Pinecone only accepts string, number, boolean, or list of strings as metadata values.
    """
    cleaned = {}
    for key, value in metadata.items():
        # Skip None values
        if value is None:
            continue
        # Handle empty lists
        if isinstance(value, list) and len(value) == 0:
            continue
        # Keep valid values
        if isinstance(value, (str, int, float, bool)):
            cleaned[key] = value
        elif isinstance(value, list):
            # Ensure list contains only strings
            string_list = [str(item) for item in value if item is not None]
            if string_list:  # Only add non-empty lists
                cleaned[key] = string_list
        else:
            # Convert other types to string
            cleaned[key] = str(value)
    
    return cleaned


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(request: UploadDocumentRequest):
    """
    Upload a single document with its vector embedding to Pinecone
    """
    try:
        store = get_vector_store()
        
        # Validate vector dimension
        if len(request.vector) != PINECONE_DIMENSION:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Vector dimension {len(request.vector)} does not match expected dimension {PINECONE_DIMENSION}"
            )
        
        # Prepare document metadata
        document_metadata = request.document.model_dump()
        
        # Generate document ID if not provided
        doc_id = request.document_id or str(uuid.uuid4())
        document_metadata['id'] = doc_id
        
        # Clean metadata to remove None values
        cleaned_metadata = clean_metadata(document_metadata)
        
        # Upload document
        success = store.add_single_document(
            document=cleaned_metadata,
            vector=request.vector,
            namespace=request.namespace
        )
        
        if success:
            logger.info(f"Successfully uploaded document with ID: {doc_id}")
            return DocumentResponse(
                success=True,
                message="Document uploaded successfully",
                document_id=doc_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload document to Pinecone"
            )
            
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading document: {str(e)}"
        )


@router.post("/upload-bulk", response_model=DocumentResponse)
async def upload_documents_bulk(request: BulkUploadDocumentRequest):
    """
    Upload multiple documents with their vector embeddings to Pinecone
    """
    try:
        store = get_vector_store()
        
        if len(request.documents) != len(request.vectors):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Number of documents must match number of vectors"
            )
        
        # Validate vector dimensions
        for i, vector in enumerate(request.vectors):
            if len(vector) != PINECONE_DIMENSION:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Vector {i} has dimension {len(vector)} but expected dimension {PINECONE_DIMENSION}"
                )
        
        # Prepare documents metadata
        documents_metadata = []
        document_ids = []
        
        for doc in request.documents:
            doc_metadata = doc.model_dump()
            doc_id = str(uuid.uuid4())
            doc_metadata['id'] = doc_id
            
            # Clean metadata to remove None values
            cleaned_metadata = clean_metadata(doc_metadata)
            documents_metadata.append(cleaned_metadata)
            document_ids.append(doc_id)
        
        # Upload documents
        success = store.add_documents(
            documents=documents_metadata,
            vectors=request.vectors,
            namespace=request.namespace
        )
        
        if success:
            logger.info(f"Successfully uploaded {len(documents_metadata)} documents")
            return DocumentResponse(
                success=True,
                message=f"Successfully uploaded {len(documents_metadata)} documents",
                document_ids=document_ids
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload documents to Pinecone"
            )
            
    except Exception as e:
        logger.error(f"Error uploading documents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading documents: {str(e)}"
        )


@router.delete("/delete", response_model=DocumentResponse)
async def delete_documents(request: DeleteDocumentRequest):
    """
    Delete documents from Pinecone by their IDs
    """
    try:
        store = get_vector_store()
        
        if not request.document_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document IDs list cannot be empty"
            )
        
        # Delete documents
        success = store.delete_documents(
            document_ids=request.document_ids,
            namespace=request.namespace
        )
        
        if success:
            logger.info(f"Successfully deleted {len(request.document_ids)} documents")
            return DocumentResponse(
                success=True,
                message=f"Successfully deleted {len(request.document_ids)} documents",
                document_ids=request.document_ids
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete documents from Pinecone"
            )
            
    except Exception as e:
        logger.error(f"Error deleting documents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting documents: {str(e)}"
        )


@router.post("/search", response_model=SimilaritySearchResponse)
async def similarity_search(request: SimilaritySearchRequest):
    """
    Search for similar documents based on vector similarity
    """
    try:
        store = get_vector_store()
        
        # Perform similarity search
        results = store.similarity_search(
            query_vector=request.query_vector,
            top_k=request.top_k,
            namespace=request.namespace,
            filter_dict=request.filter_dict
        )
        
        logger.info(f"Found {len(results)} similar documents")
        return SimilaritySearchResponse(
            success=True,
            results=results,
            total_results=len(results)
        )
        
    except Exception as e:
        logger.error(f"Error performing similarity search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing similarity search: {str(e)}"
        )


@router.get("/stats", response_model=IndexStatsResponse)
async def get_index_stats(namespace: str = ""):
    """
    Get statistics about the Pinecone index
    """
    try:
        store = get_vector_store()
        
        # Get index statistics
        stats = store.get_index_stats(namespace=namespace)
        
        return IndexStatsResponse(
            success=True,
            stats=stats
        )
        
    except Exception as e:
        logger.error(f"Error getting index stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting index stats: {str(e)}"
        )


@router.delete("/clear-namespace")
async def clear_namespace(namespace: str):
    """
    Clear all documents from a specific namespace
    """
    try:
        if not namespace:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Namespace cannot be empty"
            )
        
        store = get_vector_store()
        
        # Clear namespace
        success = store.clear_namespace(namespace=namespace)
        
        if success:
            logger.info(f"Successfully cleared namespace: {namespace}")
            return DocumentResponse(
                success=True,
                message=f"Successfully cleared namespace: {namespace}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to clear namespace: {namespace}"
            )
            
    except Exception as e:
        logger.error(f"Error clearing namespace: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing namespace: {str(e)}"
        ) 