from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from db.qdrant import QdrantWrapper
from db.redis import RedisClient
from api.routes import router
from api.pydantic import SimilarProductsRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DBs
    app.state.qdrant = QdrantWrapper()
    app.state.redis = RedisClient()
    yield
    # Close DBs
    await app.state.qdrant.close()
    await app.state.redis.close()


app = FastAPI(lifespan=lifespan)


@app.post("/similar-products-metadata")
async def get_similar_products_metadata(request: SimilarProductsRequest):
    try:
        similar_ids = app.state.qdrant.get_similar_product_option_ids(
            product_option_id=request.colorGroup_string
        )

        if request.dev.get("metadata", False):
            metadata = await app.state.redis.fetch_metadata(similar_ids)
            return {"similar_ids": similar_ids, "metadata": metadata}

        return {"similar_ids": similar_ids}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
