import sys
from pathlib import Path

# Add root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

print("start backend")

from core.repositories.jsonplaceholder_api import JsonplaceHolderRepository

jsonplacehodelRepo = JsonplaceHolderRepository()


jsonplacehodelRepo.get_user("sdsdss")

print("end backend")
