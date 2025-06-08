import datetime
import sys
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Adiciona o diretório backend ao path para as importações funcionarem
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from settings import CORS_ORIGINS, CORS_METHODS, CORS_HEADERS, APP_NAME, APP_VERSION
from api.routers.agent import router as agent_router

app = FastAPI(
    title=APP_NAME,
    description="Chat with docs conversational agent API",
    version=APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

app.include_router(agent_router)

@app.get("/status")
def check_status():
    """
    Simple status endpoint to check if the API is running.
    """
    return {
        "status": "online",
        "service": APP_NAME,        
        "version": APP_VERSION,
        "timestamp": datetime.datetime.utcnow().isoformat()
    } 