from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class DocumentMetadata(BaseModel):
    """Metadata for a document to be stored in Pinecone"""
    title: str
    content: str
    source: Optional[str] = None
    author: Optional[str] = None
    created_at: Optional[str] = None
    document_type: Optional[str] = None
    tags: Optional[List[str]] = []


class UploadDocumentRequest(BaseModel):
    """Request schema for uploading a document to Pinecone"""
    document: DocumentMetadata
    namespace: Optional[str] = ""
    document_id: Optional[str] = None
    chunk_size: Optional[int] = 1000
    chunk_overlap: Optional[int] = 200


class UploadTextRequest(BaseModel):
    """Request schema for uploading text content directly"""
    title: str
    content: str
    namespace: Optional[str] = ""
    source: Optional[str] = "text_input"
    author: Optional[str] = None
    tags: Optional[List[str]] = []
    chunk_size: Optional[int] = 1000
    chunk_overlap: Optional[int] = 200


class BulkUploadDocumentRequest(BaseModel):
    """Request schema for uploading multiple documents to Pinecone"""
    documents: List[DocumentMetadata]
    namespace: Optional[str] = ""
    chunk_size: Optional[int] = 1000
    chunk_overlap: Optional[int] = 200


class DeleteDocumentRequest(BaseModel):
    """Request schema for deleting documents from Pinecone"""
    document_ids: List[str]
    namespace: Optional[str] = ""


class SimilaritySearchRequest(BaseModel):
    """Request schema for similarity search in Pinecone"""
    query_vector: List[float]
    top_k: Optional[int] = 10
    namespace: Optional[str] = ""
    filter_dict: Optional[Dict[str, Any]] = None


class DocumentResponse(BaseModel):
    """Response schema for document operations"""
    success: bool
    message: str
    document_id: Optional[str] = None
    document_ids: Optional[List[str]] = None
    total_chunks: Optional[int] = None
    file_info: Optional[Dict[str, Any]] = None


class FileUploadResponse(BaseModel):
    """Response schema for file upload operations"""
    success: bool
    message: str
    document_id: str
    filename: str
    file_size: int
    mime_type: str
    total_chunks: int
    word_count: int
    extracted_title: str


class SimilaritySearchResponse(BaseModel):
    """Response schema for similarity search results"""
    success: bool
    results: List[Dict[str, Any]]
    total_results: int


class IndexStatsResponse(BaseModel):
    """Response schema for index statistics"""
    success: bool
    stats: Dict[str, Any] 