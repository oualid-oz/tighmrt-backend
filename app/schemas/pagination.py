from pydantic import BaseModel, Field
from typing import Optional, TypeVar, Generic, List

T = TypeVar('T')

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number starting from 1")
    size: int = Field(10, ge=1, le=100, description="Number of items per page")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    total_pages: int

    @classmethod
    def create(
        cls, 
        items: List[T], 
        total: int, 
        pagination: PaginationParams
    ) -> 'PaginatedResponse[T]':
        return cls(
            items=items,
            total=total,
            page=pagination.page,
            size=pagination.size,
            total_pages=(total + pagination.size - 1) // pagination.size
        )
