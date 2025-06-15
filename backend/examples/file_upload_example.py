"""
Example of how to use the new file upload system.
This shows the revolutionized approach where the backend does ALL the intelligence.
"""

import requests
import os
from pathlib import Path

# API endpoint
API_BASE_URL = "http://localhost:8000"

def upload_file_example():
    """Example of uploading a raw file - backend does everything!"""
    
    # Create a sample text file to test with
    sample_content = """
    Artificial Intelligence and Machine Learning

    Artificial Intelligence (AI) is a broad field of computer science concerned with building smart machines capable of performing tasks that typically require human intelligence. Machine Learning (ML) is a subset of AI that focuses on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention.

    Key Concepts in Machine Learning:

    1. Supervised Learning
    Supervised learning is the most common type of machine learning. In this approach, algorithms learn from labeled training data to make predictions or decisions about new, unseen data. Examples include:
    - Linear Regression: Predicting continuous values
    - Classification: Categorizing data into discrete classes
    - Decision Trees: Creating models that predict target values

    2. Unsupervised Learning
    Unsupervised learning involves finding hidden patterns in data without labeled examples. The algorithm tries to learn the underlying structure of the data. Common techniques include:
    - Clustering: Grouping similar data points together
    - Dimensionality Reduction: Reducing the number of features while preserving important information
    - Association Rules: Finding relationships between different variables

    3. Reinforcement Learning
    Reinforcement learning is a type of machine learning where an agent learns to make decisions by taking actions in an environment to maximize some reward. This is commonly used in:
    - Game playing (like chess or Go)
    - Robotics and autonomous systems
    - Recommendation systems

    Applications of Machine Learning:
    - Healthcare: Disease diagnosis, drug discovery, personalized treatment
    - Finance: Fraud detection, algorithmic trading, credit scoring
    - Transportation: Autonomous vehicles, traffic optimization
    - Technology: Natural language processing, computer vision, voice recognition
    - Business: Customer segmentation, demand forecasting, recommendation systems

    The future of AI and ML continues to evolve rapidly, with new breakthroughs in deep learning, neural networks, and other advanced techniques driving innovation across industries.
    """
    
    # Save to a temporary file
    temp_file_path = "temp_ml_document.txt"
    with open(temp_file_path, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    try:
        # Upload the file using FormData (super simple!)
        with open(temp_file_path, 'rb') as file:
            files = {'file': ('machine_learning_guide.txt', file, 'text/plain')}
            data = {
                'namespace': 'educational_content',
                'chunk_size': 800,
                'chunk_overlap': 150
            }
            
            print("📤 Uploading file with the new system...")
            response = requests.post(
                f"{API_BASE_URL}/documents/upload-file",
                files=files,
                data=data
            )
        
        if response.status_code == 200:
            result = response.json()
            print("🎉 File uploaded successfully with FULL AUTOMATION!")
            print(f"📄 Document ID: {result['document_id']}")
            print(f"📁 Filename: {result['filename']}")
            print(f"📏 File Size: {result['file_size']} bytes")
            print(f"🎭 MIME Type: {result['mime_type']}")
            print(f"🧩 Total Chunks: {result['total_chunks']}")
            print(f"📊 Word Count: {result['word_count']}")
            print(f"🏷️ Extracted Title: {result['extracted_title']}")
            print(f"✨ Message: {result['message']}")
        else:
            print(f"❌ Error uploading file: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
    
    finally:
        # Clean up
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def upload_text_example():
    """Example of uploading text content directly"""
    
    text_data = {
        "title": "Python Programming Basics",
        "content": """
        Python is a high-level, interpreted programming language known for its simplicity and readability. It was created by Guido van Rossum and first released in 1991.

        Key Features of Python:
        1. Easy to Learn and Use: Python has a simple syntax that mirrors the English language
        2. Interpreted Language: Python code is executed line by line
        3. Cross-platform: Python runs on Windows, macOS, Linux, and other operating systems
        4. Large Standard Library: Extensive collection of modules and functions
        5. Dynamic Typing: Variables don't need explicit declaration

        Common Python Applications:
        - Web Development (Django, Flask)
        - Data Science and Analytics (Pandas, NumPy, Matplotlib)
        - Machine Learning (Scikit-learn, TensorFlow, PyTorch)
        - Automation and Scripting
        - Desktop GUI Applications

        Python's philosophy emphasizes code readability and simplicity, making it an excellent choice for beginners and experts alike.
        """,
        "namespace": "programming_tutorials",
        "source": "educational_content",
        "tags": ["python", "programming", "tutorial"],
        "chunk_size": 600,
        "chunk_overlap": 100
    }
    
    try:
        print("📝 Uploading text content...")
        response = requests.post(
            f"{API_BASE_URL}/documents/upload-text",
            json=text_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Text uploaded successfully!")
            print(f"📄 Document ID: {result['document_id']}")
            print(f"🧩 Total chunks created: {result['total_chunks']}")
            print(f"📝 Message: {result['message']}")
        else:
            print(f"❌ Error uploading text: {response.status_code}")
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
        
        print("🔍 Testing document search...")
        
        # Create search instance
        doc_search = DocumentSearch()
        
        # Search in educational content namespace
        doc_search.thread_id = "educational_content"
        results = doc_search.search("machine learning algorithms", top_k=3)
        
        print("\n🔍 Search Results in 'educational_content':")
        print("=" * 60)
        
        for i, doc in enumerate(results, 1):
            print(f"\n{i}. {doc['title']}")
            print(f"   📊 Relevance Score: {doc['score']:.3f}")
            print(f"   🧩 Chunk: {doc['chunk_index'] + 1}/{doc['total_chunks']} ({doc['chunk_size']} chars)")
            print(f"   📄 Content Preview: {doc['content'][:150]}...")
            print(f"   📁 Source: {doc['source']}")
            print(f"   🆔 Document ID: {doc['original_document_id']}")
            print("-" * 60)
        
        # Search in programming tutorials namespace
        doc_search.thread_id = "programming_tutorials"
        results2 = doc_search.search("python programming", top_k=2)
        
        print("\n🔍 Search Results in 'programming_tutorials':")
        print("=" * 60)
        
        for i, doc in enumerate(results2, 1):
            print(f"\n{i}. {doc['title']}")
            print(f"   📊 Relevance Score: {doc['score']:.3f}")
            print(f"   🧩 Chunk: {doc['chunk_index'] + 1}/{doc['total_chunks']} ({doc['chunk_size']} chars)")
            print(f"   📄 Content Preview: {doc['content'][:150]}...")
            print(f"   📁 Source: {doc['source']}")
            print("-" * 60)
            
    except Exception as e:
        print(f"❌ Error in search: {str(e)}")


def demonstrate_file_types():
    """Show which file types are supported"""
    
    print("📋 Supported File Types:")
    print("=" * 40)
    print("✅ Text Files: .txt, .md, .log")
    print("✅ PDF Documents: .pdf")
    print("✅ Word Documents: .docx")
    print("✅ Excel Spreadsheets: .xlsx")
    print("✅ PowerPoint: .pptx")
    print("✅ Legacy Office: .doc, .xls, .ppt (limited)")
    print("✅ Other text formats with auto-detection")
    print("\n🚀 All processing is automatic:")
    print("   • Content extraction")
    print("   • Metadata generation")
    print("   • Smart chunking")
    print("   • Embedding generation")
    print("   • Pinecone storage")


if __name__ == "__main__":
    print("🚀 NEW FILE UPLOAD SYSTEM DEMONSTRATION")
    print("=" * 50)
    print("💡 Backend now does ALL the intelligence!")
    print("📁 Frontend just sends the raw file")
    print("🧠 Backend handles everything automatically")
    print("=" * 50)
    
    # Show supported file types
    demonstrate_file_types()
    
    # Test file upload
    print("\n" + "="*50)
    upload_file_example()
    
    # Test text upload
    print("\n" + "="*50)
    upload_text_example()
    
    # Test search
    print("\n" + "="*50)
    search_documents_example()
    
    print("\n🎉 DEMONSTRATION COMPLETED!")
    print("✨ The system is now truly enterprise-ready!")
    print("🚀 From amateur to professional in one refactor!") 