from dotenv import load_dotenv
import os

load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = os.getenv("QDRANT_PORT", "6333")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PREFIX = os.getenv("REDIS_PREFIX", "metadata_prefix")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "collection")