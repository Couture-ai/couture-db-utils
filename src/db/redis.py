from redis.asyncio.cluster import RedisCluster
from core.settings import REDIS_HOST, REDIS_PORT, REDIS_PREFIX
from utils import decode_response


class RedisClient:
    def __init__(self):
        self.redis_client = RedisCluster(
            host=REDIS_HOST, port=REDIS_PORT, decode_responses=False
        )

    async def fetch_metadata(self, ids: list) -> list:
        pipe = self.redis_client.pipeline()
        for sku in ids:
            key = f"{REDIS_PREFIX}:{sku}"
            pipe.get(key)
        raw_data = await pipe.execute()

        decoded_data = []
        for item in raw_data:
            parsed = decode_response(item)
            decoded_data.append(parsed)

        return decoded_data
