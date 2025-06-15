"""
Example of how to upload documents using the new chunking system.
This example shows how documents are automatically chunked and embedded.
"""

import requests
import json

# API endpoint
API_BASE_URL = "http://localhost:8000"

def upload_document_example():
    """Example of uploading a single document with chunking"""
    
    document_data = {
        "document": {
            "title": "Introduction to Machine Learning",
            "content": """
            Machine learning is a subset of artificial intelligence (AI) that focuses on the development of algorithms and statistical models that enable computers to improve their performance on a specific task through experience, without being explicitly programmed to do so.

            The core idea behind machine learning is to build systems that can learn from data. These systems analyze patterns in data and make predictions or decisions based on what they have learned. This approach is particularly useful when it's difficult or impossible to write explicit rules for solving a problem.

            There are several types of machine learning:

            1. Supervised Learning: This involves training a model on a labeled dataset, where the correct answers are provided. The model learns to map inputs to outputs based on these examples. Common algorithms include linear regression, decision trees, and neural networks.

            2. Unsupervised Learning: Here, the model finds patterns in data without being given the correct answers. Clustering and dimensionality reduction are common unsupervised learning tasks.

            3. Reinforcement Learning: This involves an agent learning to make decisions by interacting with an environment and receiving rewards or penalties for its actions.

            Machine learning has applications in many fields, including healthcare, finance, transportation, and entertainment. As data continues to grow in volume and complexity, machine learning becomes increasingly important for extracting insights and making data-driven decisions.

            The field is rapidly evolving, with new techniques and applications being developed constantly. Deep learning, a subset of machine learning based on neural networks, has been particularly successful in recent years for tasks like image recognition and natural language processing.
            """,
            "source": "educational_content",
            "author": "AI Education Team",
            "document_type": "article",
            "tags": ["machine learning", "AI", "education"]
        },
        "namespace": "educational_docs",
        "chunk_size": 500,
        "chunk_overlap": 100
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/documents/upload",
            json=document_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Document uploaded successfully!")
            print(f"📄 Document ID: {result['document_id']}")
            print(f"🧩 Total chunks created: {result['total_chunks']}")
            print(f"📝 Message: {result['message']}")
        else:
            print(f"❌ Error uploading document: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")


def search_documents_example():
    """Example of searching for documents using the DocumentSearch class"""
    
    try:
        # Import the search functionality
        import sys
        sys.path.append('.')
        from agent.agent_toolbox.tools.doc_search import DocumentSearch
        
        # Create search instance
        doc_search = DocumentSearch()
        
        # Search in specific namespace
        doc_search.thread_id = "educational_docs"
        
        # Perform search
        results = doc_search.search("what is supervised learning?", top_k=3)
        
        print("\n🔍 Search Results:")
        print("=" * 50)
        
        for i, doc in enumerate(results, 1):
            print(f"\n{i}. {doc['title']}")
            print(f"   📊 Score: {doc['score']:.3f}")
            print(f"   🧩 Chunk: {doc['chunk_index'] + 1}/{doc['total_chunks']} ({doc['chunk_size']} chars)")
            print(f"   📄 Content: {doc['content'][:200]}...")
            print(f"   📁 Source: {doc['source']}")
            print(f"   🆔 Document ID: {doc['original_document_id']}")
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Error in search: {str(e)}")


if __name__ == "__main__":
    print("🚀 Document Upload and Search Example")
    print("=" * 50)
    
    # First, upload a document
    print("\n📤 Uploading document...")
    upload_document_example()
    
    # Then search for it
    print("\n🔍 Searching documents...")
    search_documents_example()
    
    print("\n✅ Example completed!") 