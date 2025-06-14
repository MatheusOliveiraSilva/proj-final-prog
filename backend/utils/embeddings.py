import openai
from typing import List
import logging
from settings import OPENAI_API_KEY

# Configure logging
logger = logging.getLogger(__name__)

def get_openai_embedding(text: str, model: str = "text-embedding-3-large") -> List[float]:
    """
    Generate embedding for text using OpenAI API
    
    Args:
        text (str): Text to embed
        model (str): OpenAI embedding model to use
        
    Returns:
        List[float]: Embedding vector
    """
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.embeddings.create(
            model=model,
            input=text
        )
        
        embedding = response.data[0].embedding
        logger.debug(f"Generated embedding with {len(embedding)} dimensions using {model}")
        
        return embedding
        
    except Exception as e:
        logger.error(f"Error generating embedding with OpenAI: {str(e)}")
        raise


def get_embedding_batch(texts: List[str], model: str = "text-embedding-3-large") -> List[List[float]]:
    """
    Generate embeddings for multiple texts in batch
    
    Args:
        texts (List[str]): List of texts to embed
        model (str): OpenAI embedding model to use
        
    Returns:
        List[List[float]]: List of embedding vectors
    """
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.embeddings.create(
            model=model,
            input=texts
        )
        
        embeddings = [data.embedding for data in response.data]
        logger.info(f"Generated {len(embeddings)} embeddings using {model}")
        
        return embeddings
        
    except Exception as e:
        logger.error(f"Error generating batch embeddings with OpenAI: {str(e)}")
        raise 