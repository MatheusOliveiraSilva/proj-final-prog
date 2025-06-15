from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form
from typing import List, Optional
import uuid
import logging

from vector_store.pinecone_utils import PineconeVectorStore
from utils.text_chunking import chunk_document, chunk_documents_batch
from utils.embeddings import get_embedding_batch
from utils.file_processing import (
    detect_file_type, 
    extract_text_content, 
    generate_document_metadata, 
    validate_file_upload
)
from settings import PINECONE_INDEX_NAME, PINECONE_DIMENSION
from api.schemas.document_schemas import (
    UploadDocumentRequest,
    UploadTextRequest,
    BulkUploadDocumentRequest,
    DeleteDocumentRequest,
    SimilaritySearchRequest,
    DocumentResponse,
    FileUploadResponse,
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
    Upload a single document with automatic chunking and vector embedding to Pinecone
    """
    try:
        store = get_vector_store()
        
        # Prepare document metadata
        document_metadata = request.document.model_dump()
        
        # Generate document ID if not provided
        doc_id = request.document_id or str(uuid.uuid4())
        document_metadata['id'] = doc_id
        
        # Chunk the document with custom parameters
        chunks = chunk_document(
            document_metadata, 
            chunk_size=request.chunk_size, 
            chunk_overlap=request.chunk_overlap
        )
        
        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document could not be chunked - possibly empty content"
            )
        
        logger.info(f"Created {len(chunks)} chunks for document {doc_id}")
        
        # Generate embeddings for all chunks
        chunk_texts = [chunk['content'] for chunk in chunks]
        chunk_embeddings = get_embedding_batch(chunk_texts)
        
        # Validate dimensions
        for i, embedding in enumerate(chunk_embeddings):
            if len(embedding) != PINECONE_DIMENSION:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Embedding {i} has dimension {len(embedding)} but expected {PINECONE_DIMENSION}"
                )
        
        # Clean metadata for all chunks
        cleaned_chunks = []
        for chunk in chunks:
            cleaned_chunk = clean_metadata(chunk)
            cleaned_chunks.append(cleaned_chunk)
        
        # Upload chunks to Pinecone
        success = store.add_documents(
            documents=cleaned_chunks,
            vectors=chunk_embeddings,
            namespace=request.namespace
        )
        
        if success:
            logger.info(f"Successfully uploaded document {doc_id} as {len(chunks)} chunks")
            return DocumentResponse(
                success=True,
                message=f"Document uploaded successfully as {len(chunks)} chunks",
                document_id=doc_id,
                total_chunks=len(chunks)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload document chunks to Pinecone"
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
    Upload multiple documents with automatic chunking and vector embeddings to Pinecone
    """
    try:
        store = get_vector_store()
        
        # Prepare documents metadata
        documents_metadata = []
        document_ids = []
        
        for doc in request.documents:
            doc_metadata = doc.model_dump()
            doc_id = str(uuid.uuid4())
            doc_metadata['id'] = doc_id
            documents_metadata.append(doc_metadata)
            document_ids.append(doc_id)
        
        # Chunk all documents with custom parameters
        all_chunks = chunk_documents_batch(
            documents_metadata, 
            chunk_size=request.chunk_size, 
            chunk_overlap=request.chunk_overlap
        )
        
        if not all_chunks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid chunks could be created from the provided documents"
            )
        
        logger.info(f"Created {len(all_chunks)} total chunks for {len(documents_metadata)} documents")
        
        # Generate embeddings for all chunks
        chunk_texts = [chunk['content'] for chunk in all_chunks]
        chunk_embeddings = get_embedding_batch(chunk_texts)
        
        # Validate dimensions
        for i, embedding in enumerate(chunk_embeddings):
            if len(embedding) != PINECONE_DIMENSION:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Embedding {i} has dimension {len(embedding)} but expected {PINECONE_DIMENSION}"
                )
        
        # Clean metadata for all chunks
        cleaned_chunks = []
        for chunk in all_chunks:
            cleaned_chunk = clean_metadata(chunk)
            cleaned_chunks.append(cleaned_chunk)
        
        # Upload chunks to Pinecone
        success = store.add_documents(
            documents=cleaned_chunks,
            vectors=chunk_embeddings,
            namespace=request.namespace
        )
        
        if success:
            logger.info(f"Successfully uploaded {len(documents_metadata)} documents as {len(all_chunks)} chunks")
            return DocumentResponse(
                success=True,
                message=f"Successfully uploaded {len(documents_metadata)} documents as {len(all_chunks)} chunks",
                document_ids=document_ids,
                total_chunks=len(all_chunks)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload document chunks to Pinecone"
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


@router.post("/upload-file", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    namespace: Optional[str] = Form(""),
    chunk_size: Optional[int] = Form(1000),
    chunk_overlap: Optional[int] = Form(200)
):
    """
    Upload a file and automatically extract content, generate metadata, chunk, and embed it.
    Supports: PDF, Word (DOCX), Excel, PowerPoint, Text files, and more.
    """
    try:
        store = get_vector_store()
        
        # Read file content
        file_content = await file.read()
        filename = file.filename or "unknown_file"
        
        logger.info(f"Processing file upload: {filename} ({len(file_content)} bytes)")
        
        # Validate file
        is_valid, error_message = validate_file_upload(filename, file_content)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        # Detect file type
        mime_type, file_extension = detect_file_type(filename, file_content)
        logger.info(f"Detected file type: {mime_type} ({file_extension})")
        
        # Extract text content
        extracted_content = extract_text_content(file_content, mime_type, filename)
        
        if not extracted_content or len(extracted_content.strip()) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract meaningful text content from the file"
            )
        
        # Generate metadata automatically
        document_metadata = generate_document_metadata(
            filename=filename,
            content=extracted_content,
            mime_type=mime_type,
            file_size=len(file_content),
            namespace=namespace
        )
        
        logger.info(f"Generated metadata for {filename}: {document_metadata['word_count']} words")
        
        # Chunk the document
        chunks = chunk_document(
            document_metadata, 
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
        
        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document could not be chunked - possibly empty content"
            )
        
        logger.info(f"Created {len(chunks)} chunks for {filename}")
        
        # Generate embeddings for all chunks
        chunk_texts = [chunk['content'] for chunk in chunks]
        chunk_embeddings = get_embedding_batch(chunk_texts)
        
        # Validate dimensions
        for i, embedding in enumerate(chunk_embeddings):
            if len(embedding) != PINECONE_DIMENSION:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Embedding {i} has dimension {len(embedding)} but expected {PINECONE_DIMENSION}"
                )
        
        # Clean metadata for all chunks
        cleaned_chunks = []
        for chunk in chunks:
            cleaned_chunk = clean_metadata(chunk)
            cleaned_chunks.append(cleaned_chunk)
        
        # Upload chunks to Pinecone
        success = store.add_documents(
            documents=cleaned_chunks,
            vectors=chunk_embeddings,
            namespace=namespace
        )
        
        if success:
            logger.info(f"Successfully uploaded {filename} as {len(chunks)} chunks")
            return FileUploadResponse(
                success=True,
                message=f"File '{filename}' uploaded and processed successfully",
                document_id=document_metadata['id'],
                filename=filename,
                file_size=len(file_content),
                mime_type=mime_type,
                total_chunks=len(chunks),
                word_count=document_metadata['word_count'],
                extracted_title=document_metadata['title']
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload document chunks to Pinecone"
            )
            
    except Exception as e:
        logger.error(f"Error processing file upload {filename}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )


@router.post("/upload-text", response_model=DocumentResponse)
async def upload_text(request: UploadTextRequest):
    """
    Upload text content directly (for when user types/pastes content)
    """
    try:
        store = get_vector_store()
        
        # Create document metadata from request
        document_metadata = {
            'id': str(uuid.uuid4()),
            'title': request.title,
            'content': request.content,
            'source': request.source,
            'author': request.author,
            'created_at': f"{__import__('datetime').datetime.utcnow().isoformat()}",
            'document_type': 'text_input',
            'tags': request.tags or [],
            'word_count': len(request.content.split()),
            'char_count': len(request.content),
            'namespace': request.namespace
        }
        
        # Chunk the document
        chunks = chunk_document(
            document_metadata, 
            chunk_size=request.chunk_size, 
            chunk_overlap=request.chunk_overlap
        )
        
        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text could not be chunked - possibly empty content"
            )
        
        logger.info(f"Created {len(chunks)} chunks for text input: '{request.title}'")
        
        # Generate embeddings for all chunks
        chunk_texts = [chunk['content'] for chunk in chunks]
        chunk_embeddings = get_embedding_batch(chunk_texts)
        
        # Clean metadata for all chunks
        cleaned_chunks = []
        for chunk in chunks:
            cleaned_chunk = clean_metadata(chunk)
            cleaned_chunks.append(cleaned_chunk)
        
        # Upload chunks to Pinecone
        success = store.add_documents(
            documents=cleaned_chunks,
            vectors=chunk_embeddings,
            namespace=request.namespace
        )
        
        if success:
            logger.info(f"Successfully uploaded text '{request.title}' as {len(chunks)} chunks")
            return DocumentResponse(
                success=True,
                message=f"Text '{request.title}' uploaded successfully as {len(chunks)} chunks",
                document_id=document_metadata['id'],
                total_chunks=len(chunks)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload text chunks to Pinecone"
            )
            
    except Exception as e:
        logger.error(f"Error uploading text: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading text: {str(e)}"
        ) 