from typing import List, Optional
import requests
from beartype import beartype
from beartype.roar import BeartypeCallHintParamViolation
from core.models.repo_jsonplacehodel import User
from core.repositories.jsonplaceholder import jsonplaceHolderRepository


class JsonplaceHolderRepository(jsonplaceHolderRepository):
    """Adapter that fetches data from JSONPlaceholder API"""

    @beartype
    def __init__(self, url: str = "https://jsonplaceholder.typicode.com"):
        self.url = url

    @beartype
    def get_user(self, user_id: int) -> Optional[User]:
        """Fetch user from JSONPlaceholder API

        Args:
            user_id: User ID (must be int, not string)

        Returns:
            User object or None if not found

        Raises:
            BeartypeCallHintParamViolation: If user_id is not an int
        """
        try:
            # Build API URL
            endpoint = f"{self.url}/users/{user_id}"
            print(f"Fetching from: {endpoint}")

            # Make HTTP GET request
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Map API response to User model
            user = User(
                id=data.get("id"),
                name=data.get("name"),
                username=data.get("username"),
                email=data.get("email"),
                address=data.get("address"),
                phone=data.get("phone"),
                website=data.get("website"),
                company=data.get("company"),
            )
            print(f"User found: {user.name}")
            return user

        except requests.exceptions.RequestException as e:
            print(f"Error fetching user {user_id}: {e}")
            return None
        except (ValueError, KeyError) as e:
            print(f"Error processing user data: {e}")
            return None
