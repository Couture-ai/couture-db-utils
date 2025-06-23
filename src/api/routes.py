from fastapi import FastAPI, Request, HTTPException
from fastapi.routing import APIRouter
from .pydantic import SimilarProductsRequest, SimilarProductsResponse

router = APIRouter()


@router.post("/similar-products-metadata", response_model=SimilarProductsResponse)
async def get_similar_products_metadata(request: Request, body: SimilarProductsRequest):
    try:
        qdrant_client = request.app.state.qdrant
        redis_client = request.app.state.redis

        similar_ids = qdrant_client.get_similar_product_option_ids(
            product_option_id=body.colorGroup_string
        )

        metadata = None
        if body.dev.get("metadata", False):
            metadata = await redis_client.get_product_metadata_redis(similar_ids)

        return SimilarProductsResponse(similar_ids=similar_ids, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
