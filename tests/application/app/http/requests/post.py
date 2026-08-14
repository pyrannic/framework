from pydantic import BaseModel, Field


class PostRequest(BaseModel):
    title: str = Field(description="Post Title")
    content: str = Field(description="Post Content")
