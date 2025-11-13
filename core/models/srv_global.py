from dataclasses import dataclass


@dataclass
class ResponseModel:
    status: bool
    code: int
    message: str
    data: any
