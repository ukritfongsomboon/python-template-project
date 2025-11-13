import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# Get environment variables
api_url = os.getenv("API_URL", "https://jsonplaceholder.typicode.com")
debug_mode = os.getenv("DEBUG", "False").lower() == "true"


# Application setup
from fastapi import FastAPI
from core.repositories.jsonplaceholder_api import JsonplaceHolderRepository
from core.services.user_srv import UserService
from core.handlers.user_res import userHandler


# Repositories
jsonplacehodelRepo = JsonplaceHolderRepository(api_url)

# Services
userSrv = UserService(jsonplacehodelRepo)

# Handlers
userHand = userHandler(userSrv)


app = FastAPI(title="User API", version="1.0.0")


# FastAPI endpoints
@app.get("/api/users")
async def get_users():
    return await userHand.list_users_handler()


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint

    Returns:
        dict: Status of the application
    """
    return {"status": "healthy", "message": "API is running"}


# Application startup
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info" if debug_mode else "warning",
    )
