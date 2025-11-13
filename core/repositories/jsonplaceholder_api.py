from typing import List
import requests
from beartype import beartype
from beartype.roar import BeartypeCallHintParamViolation
from core.models.repo_jsonplacehodel import User, RepoCommentModel
from core.repositories.jsonplaceholder import jsonplaceHolderRepository


class JsonplaceHolderRepository(jsonplaceHolderRepository):
    """Adapter that fetches data from JSONPlaceholder API"""

    @beartype
    def __init__(self, url: str = "https://jsonplaceholder.typicode.com"):
        self.url = url

    @beartype
    def get_users(self) -> List[User]:
        """Fetch all users from JSONPlaceholder API

        Returns:
            List of User objects

        Raises:
            BeartypeCallHintParamViolation: If return type is not List[User]
        """
        try:
            # Build API URL
            endpoint = f"{self.url}/users"
            # print(f"Fetching from: {endpoint}")

            # Make HTTP GET request
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()

            data = response.json()

            # print(f"API Response: Got {len(data)} users")

            # Map API response to User models
            users = []
            for user_data in data:
                user = User(
                    id=user_data.get("id"),
                    name=user_data.get("name"),
                    username=user_data.get("username"),
                    email=user_data.get("email"),
                    address=user_data.get("address"),
                    phone=user_data.get("phone"),
                    website=user_data.get("website"),
                    company=user_data.get("company"),
                )
                users.append(user)
                # print(f"User loaded: {user.name}")

            # print(f"Total users loaded: {len(users)}")
            return users

        except requests.exceptions.RequestException as e:
            print(f"Error fetching users: {e}")
            return []
        except (ValueError, KeyError) as e:
            print(f"Error processing user data: {e}")
            return []

    @beartype
    def get_comments(self) -> List[RepoCommentModel]:
        """Fetch all comments from JSONPlaceholder API

        Returns:
            List of RepoCommentModel objects

        Raises:
            BeartypeCallHintParamViolation: If return type is not List[RepoCommentModel]
        """
        try:
            # Build API URL
            endpoint = f"{self.url}/comments"
            # print(f"Fetching from: {endpoint}")

            # Make HTTP GET request
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()

            data = response.json()

            # print(f"API Response: Got {len(data)} comments")

            # Map API response to RepoCommentModel models
            comments = []
            for comment_data in data:
                comment = RepoCommentModel(
                    postId=comment_data.get("postId"),
                    id=comment_data.get("id"),
                    name=comment_data.get("name"),
                    email=comment_data.get("email"),
                    body=comment_data.get("body"),
                )
                comments.append(comment)
                # print(f"Comment loaded: {comment.name}")

            # print(f"Total comments loaded: {len(comments)}")
            return comments

        except requests.exceptions.RequestException as e:
            print(f"Error fetching comments: {e}")
            return []
        except (ValueError, KeyError) as e:
            print(f"Error processing comments data: {e}")
            return []
