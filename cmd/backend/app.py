import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

print("start backend")

# Get environment variables
api_url = os.getenv("API_URL", "https://jsonplaceholder.typicode.com")
debug_mode = os.getenv("DEBUG", "False").lower() == "true"

# if debug_mode:
#     print(f"Debug Mode: ON")
#     print(f"API URL: {api_url}")

from core.repositories.jsonplaceholder_api import JsonplaceHolderRepository
from beartype.roar import BeartypeCallHintParamViolation

jsonplacehodelRepo = JsonplaceHolderRepository(api_url)

users = jsonplacehodelRepo.get_users()
print(users)

print("\nend backend")
