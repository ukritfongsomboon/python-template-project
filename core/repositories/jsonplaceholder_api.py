from typing import List, Optional
from core.models.repo_jsonplacehodel import User
from core.repositories.jsonplaceholder import jsonplaceHolderRepository


class JsonplaceHolderRepository(jsonplaceHolderRepository):
    """Adapter ที่เก็บข้อมูลในหน่วยความจำ (mock)"""

    def __init__(self, url: str):
        from core.models.repo_jsonplacehodel import Address, Company, Geo

        self.url = url
        self.users = [
            User(
                id=1,
                name="Alice",
                username="alice",
                email="alice@example.com",
                address=Address(
                    street="123 Main St",
                    suite="Suite 1",
                    city="NYC",
                    zipcode="10001",
                    geo=Geo(lat="40.7128", lng="-74.0060"),
                ),
                phone="555-1234",
                website="alice.com",
                company=Company(name="Acme", catchPhrase="Innovation", bs="solutions"),
            ),
            User(
                id=2,
                name="Bob",
                username="bob",
                email="bob@example.com",
                address=Address(
                    street="456 Oak Ave",
                    suite="Suite 2",
                    city="LA",
                    zipcode="90001",
                    geo=Geo(lat="34.0522", lng="-118.2437"),
                ),
                phone="555-5678",
                website="bob.com",
                company=Company(
                    name="TechCorp", catchPhrase="Forward thinking", bs="tech"
                ),
            ),
        ]

    def get_user(self, user_id: int) -> Optional[User]:
        print("get_user", user_id)
        print(self.url)
        return next((user for user in self.users if user.id == user_id), None)
