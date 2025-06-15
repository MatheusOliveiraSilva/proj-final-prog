from dotenv import load_dotenv
import os

load_dotenv()

# Agent Stuff
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Pinecone Configuration
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "chatwithdocs")
PINECONE_DIMENSION = int(os.getenv("PINECONE_DIMENSION", "3072"))

# API Stuff
APP_NAME = "Agent API"
APP_VERSION = "0.1.0"

# CORS Stuff
CORS_ORIGINS = ["*"]
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]