from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict, Any
import uuid
import logging

# Configure logging
logger = logging.getLogger(__name__)

def chunk_document(
    document: Dict[str, Any], 
    chunk_size: int = 1000, 
    chunk_overlap: int = 200
) -> List[Dict[str, Any]]:
    """
    Break a document into smaller chunks using RecursiveCharacterTextSplitter.
    
    Args:
        document (Dict[str, Any]): Document with metadata
        chunk_size (int): Maximum size of each chunk (default: 1000)
        chunk_overlap (int): Overlap between chunks (default: 200)
        
    Returns:
        List[Dict[str, Any]]: List of document chunks with metadata
    """
    try:
        # Get the document content
        content = document.get('content', '')
        if not content:
            logger.warning(f"Document {document.get('id', 'unknown')} has no content to chunk")
            return []
        
        # Create text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Split the text into chunks
        chunks = text_splitter.split_text(content)
        
        logger.info(f"Split document '{document.get('title', 'unknown')}' into {len(chunks)} chunks")
        
        # Create chunk documents
        chunk_documents = []
        original_doc_id = document.get('id', str(uuid.uuid4()))
        
        for i, chunk_text in enumerate(chunks):
            chunk_doc = {
                'id': f"{original_doc_id}_chunk_{i}",
                'content': chunk_text,
                'title': document.get('title', 'Unknown'),
                'source': document.get('source', 'Unknown'),
                'author': document.get('author'),
                'created_at': document.get('created_at'),
                'document_type': document.get('document_type'),
                'tags': document.get('tags', []),
                # Add chunk-specific metadata
                'original_document_id': original_doc_id,
                'chunk_index': i,
                'total_chunks': len(chunks),
                'chunk_size': len(chunk_text)
            }
            chunk_documents.append(chunk_doc)
        
        return chunk_documents
        
    except Exception as e:
        logger.error(f"Error chunking document: {str(e)}")
        return []


def chunk_documents_batch(
    documents: List[Dict[str, Any]], 
    chunk_size: int = 1000, 
    chunk_overlap: int = 200
) -> List[Dict[str, Any]]:
    """
    Chunk multiple documents in batch.
    
    Args:
        documents (List[Dict[str, Any]]): List of documents to chunk
        chunk_size (int): Maximum size of each chunk (default: 1000)
        chunk_overlap (int): Overlap between chunks (default: 200)
        
    Returns:
        List[Dict[str, Any]]: List of all document chunks
    """
    try:
        all_chunks = []
        
        for doc in documents:
            chunks = chunk_document(doc, chunk_size, chunk_overlap)
            all_chunks.extend(chunks)
        
        logger.info(f"Chunked {len(documents)} documents into {len(all_chunks)} total chunks")
        return all_chunks
        
    except Exception as e:
        logger.error(f"Error chunking documents batch: {str(e)}")
        return []


def get_chunk_info(chunk_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract chunk information from metadata.
    
    Args:
        chunk_metadata (Dict[str, Any]): Chunk metadata
        
    Returns:
        Dict[str, Any]: Formatted chunk information
    """
    return {
        'chunk_id': chunk_metadata.get('id'),
        'original_document_id': chunk_metadata.get('original_document_id'),
        'chunk_index': chunk_metadata.get('chunk_index', 0),
        'total_chunks': chunk_metadata.get('total_chunks', 1),
        'chunk_size': chunk_metadata.get('chunk_size', 0),
        'title': chunk_metadata.get('title', 'Unknown'),
        'content_preview': chunk_metadata.get('content', '')[:100] + '...' if len(chunk_metadata.get('content', '')) > 100 else chunk_metadata.get('content', '')
    } 