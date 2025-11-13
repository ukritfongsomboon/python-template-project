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

# if debug_mode:
#     print(f"Debug Mode: ON")
#     print(f"API URL: {api_url}")

from core.repositories.jsonplaceholder_api import JsonplaceHolderRepository
from core.services.user_srv import UserService


# Repositories
jsonplacehodelRepo = JsonplaceHolderRepository(api_url)

# Services
userSrv = UserService(jsonplacehodelRepo)

# Handlers


res = userSrv.getAllUser()
print(res)
