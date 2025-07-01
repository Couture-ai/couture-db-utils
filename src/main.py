from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.qdrant import QdrantWrapper
from db.redis import RedisClient
from api import api_router, qdrant_router
from starlette.datastructures import State


class DBUtilsAppState(State):
    qdrant: QdrantWrapper
    redis: RedisClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DBs
    app.state = DBUtilsAppState()

    app.state.qdrant = QdrantWrapper()
    app.state.redis = RedisClient()

    yield
    # Close DBs
    # await app.state.qdrant.close()
    # await app.state.redis.close()


app = FastAPI(lifespan=lifespan)

# Allow Magento frontend to call FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)
app.include_router(qdrant_router, prefix="/api")  # subrouter for /api like: /api/qdrant
