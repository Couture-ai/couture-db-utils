from fastapi import APIRouter, Request, Depends
from .pydantic import QdrantSearchRequest
from db.qdrant import QdrantWrapper


def get_qdrant_client(request: Request) -> QdrantWrapper:
    return request.app.state.qdrant


qdrant_router = APIRouter(prefix="/qdrant")


@qdrant_router.post("/get_id_info")
def get_qdrant_metadata(
    request: QdrantSearchRequest, q_client: QdrantWrapper = Depends(get_qdrant_client)
):
    results = q_client.get_qdrant_metadata(
        point_id=request.point_id,
        colorGroup_string=request.colorGroup_string,
    )
    return results
