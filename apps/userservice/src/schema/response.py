from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar("T")


# 基础响应（非分页）
class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: Optional[T] = None


# 分页数据容器（放在 data 里）
class PageData(BaseModel, Generic[T]):
    records: List[T]
    total: int
    page: int
    size: int


# 分页响应（data 字段类型为 PageData[T]）
class PageResponse(ApiResponse[PageData[T]]):
    pass


class ErrorResponse(BaseModel):
    code: int = 400
    message: str = "出错了"
