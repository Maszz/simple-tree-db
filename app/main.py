"""
FastAPI application for managing a tree-like data structure.

This script provides a RESTful API for performing operations on a tree database. 
It includes functionalities for creating, querying, updating, and deleting nodes 
in the tree. The application uses Pydantic models for request and response validation, 
and the tree data is managed using a TreeDataBase instance.

The API endpoints are as follows:
- `/`: Returns a simple greeting message.
- `/items/query_tree`: Retrieves the entire tree structure.
- `/items/`: Gets a specific node or all child nodes based on the provided node identifier.
- `/items` (POST): Creates a new node in the tree.
- `/items/update` (POST): Updates an existing node in the tree.
- `/items/delete` (POST): Deletes a node from the tree.

Error handling is implemented to manage common scenarios like missing nodes or invalid requests.

To run the application, Uvicorn, an ASGI server, is used. The application's configuration is managed
through environment variables and a settings class. The tree data can be persisted to and loaded from a file.

Attributes:
    app (FastAPI): The FastAPI application instance.
    db_proxy (TreeDataBase): The tree database proxy for data operations.
    settings (Settings): Application settings loaded from environment variables.

Functions:
    get_settings(): Caches and retrieves application settings.

Usage:
    Run the script using a command like `uvicorn script_name:app` to start the server.

Note:
    The script depends on external modules like FastAPI, Pydantic, and Uvicorn, 
    and requires the TreeDataBase class for tree data operations.
"""
from fastapi import FastAPI, HTTPException
from TreeDataBase import TreeDataBase
from pydantic import BaseModel
from typing import Union, Any, Dict
import uvicorn
from typing import Optional
from core.dto import (
    CreateRequestDto,
    UpdateRequestDto,
    DeleteRequestDto,
    GetAllResponsesDto,
    GetResponsetDto,
    HttpResponseDto,
    QueryTreeResponseDto,
)
from fastapi import status
from core.config import Settings
from functools import lru_cache


# from db_proxy import db_proxy

# DB_PATH = "data.db"
# DB_ROOT_NODE = "o=ผ้าปู"


@lru_cache
def get_settings():
    return Settings()


app = FastAPI()
db_proxy = TreeDataBase()
settings = get_settings()
data = db_proxy.load_from_file(settings.DB_PATH, root_id=settings.DB_ROOT_NODE)


@app.get("/")
async def root():
    return {"message": "Hello DataStructure 1"}


@app.get("/items/query_tree")
async def query_tree() -> QueryTreeResponseDto:
    d = db_proxy.get_tree()
    return {
        "tree": d,
    }


@app.get("/items/", status_code=status.HTTP_200_OK)
async def read_item(
    node_id: Optional[str] = None,
) -> Union[GetResponsetDto, GetAllResponsesDto]:
    print(node_id)
    if node_id is None:
        res = db_proxy.get_all_children()

        return GetAllResponsesDto(all=res)
    res = db_proxy.query(node_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return GetResponsetDto(id=str(res.id), data=res.data, node_id=node_id)


@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(create_dto: CreateRequestDto) -> HttpResponseDto:
    b, s = db_proxy.insert(create_dto.data, create_dto.node_id)
    if not b:
        raise HTTPException(status_code=400, detail=s)

    return HttpResponseDto(status="200", message="OK")


@app.post("/items/update", status_code=status.HTTP_200_OK)
async def update_item(dto: UpdateRequestDto) -> HttpResponseDto:
    b, s = db_proxy.update(dto.node_id, dto.data)
    if not b:
        raise HTTPException(status_code=400, detail=s)

    return HttpResponseDto(status="200", message="OK")


@app.post("/items/delete", status_code=status.HTTP_200_OK)
async def delete_item(dto: DeleteRequestDto) -> HttpResponseDto:
    b, s = db_proxy.delete(dto.node_id)
    if not b:
        raise HTTPException(status_code=400, detail=s)

    return HttpResponseDto(status="200", message="OK")


# Path: ApiServer.py

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
