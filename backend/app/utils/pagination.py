from math import ceil
from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = 1
    size: int = 20

    @property
    def offset(self) -> int:
        return (max(self.page, 1) - 1) * max(self.size, 1)

    @property
    def limit(self) -> int:
        return max(self.size, 1)


class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

    @classmethod
    def create(cls, items: List[T], total: int, params: PaginationParams) -> "Page[T]":
        pages = ceil(total / params.size) if params.size > 0 else 0
        return cls(
            items=items,
            total=total,
            page=params.page,
            size=params.size,
            pages=pages,
        )
