from dataclasses import dataclass


@dataclass
class SrvCommentModel:
    postId: int
    id: int
    name: str
    email: str
    body: str
