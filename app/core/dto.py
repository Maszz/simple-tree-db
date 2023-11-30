from typing import Union, Any, Dict, List, Optional
from pydantic import BaseModel


class CreateRequestDto(BaseModel):
    node_id: str
    data: Dict[str, Any]


class UpdateRequestDto(BaseModel):
    node_id: str
    data: Dict[str, Any]


class DeleteRequestDto(BaseModel):
    node_id: str


class GetResponsetDto(BaseModel):
    id: str
    data: Dict[str, Any]
    node_id: str


class GetAllResponsesDto(BaseModel):
    all: List[Dict[str, Any]]


class HttpResponseDto(BaseModel):
    status: str
    message: Optional[str] = None


class QueryTreeResponseDto(BaseModel):
    tree: Dict[str, Any]
