from pydantic import BaseModel, HttpUrl, Field


class URLRequest(BaseModel):
    """
    Request schema for URL scanning.
    """

    url: HttpUrl = Field(
        ...,
        description="URL to scan"
    )


class URLResponse(BaseModel):
    """
    Response schema for URL scan results.
    """

    url: str
    safe: bool
    risk_score: int
    ssl: bool
    blacklisted: bool
    message: str