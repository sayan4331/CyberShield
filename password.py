from pydantic import BaseModel, Field


class PasswordRequest(BaseModel):
    """
    Request schema for password strength checking.
    """

    password: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="Password to evaluate"
    )


class PasswordResponse(BaseModel):
    """
    Response schema for password strength analysis.
    """

    strength: str
    score: int
    entropy: float
    crack_time: str
    feedback: list[str]