from pydantic import BaseModel


class QuestionRequest(BaseModel):
    """Request model for chat queries."""
    question: str


class RagToolInput(BaseModel):
    """Input schema for the RAG retriever tool."""
    question: str
