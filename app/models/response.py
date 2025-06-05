from typing import Generic, TypeVar, List, Optional, Dict, Any
from pydantic import BaseModel, Field

T = TypeVar('T')


class ResponseBase(BaseModel):
    """Base response model for all API responses"""
    success: bool = True
    message: str = "Operation completed successfully"


class ResponseWithData(ResponseBase, Generic[T]):
    """Response model with data"""
    data: T


class PaginatedResponse(ResponseBase, Generic[T]):
    """Response model with pagination metadata"""
    data: List[T]
    page: int
    page_size: int
    total: int
    total_pages: int


class ErrorResponse(ResponseBase):
    """Error response model"""
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class HealthCheckResponse(ResponseBase):
    """Health check response model"""
    status: str = "ok"
    version: str
    environment: str
