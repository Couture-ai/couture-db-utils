from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from core.settings import QDRANT_HOST, QDRANT_PORT, COLLECTION_NAME
from typing import Union


class QdrantWrapper:
    def __init__(self):
        url = f"http://{QDRANT_HOST}:{QDRANT_PORT}"
        self.client = QdrantClient(url=url, timeout=10000)
        print("Qdrant Client initialized")

    def get_similar_product_option_ids(
        self,
        product_option_id: str,
        limit: int = 10,
        must_filters: dict = None,
        should_filters: dict = None,
    ) -> list:
        try:
            scroll_result = self.client.scroll(
                collection_name=COLLECTION_NAME,
                scroll_filter=qdrant_models.Filter(
                    must=[
                        qdrant_models.FieldCondition(
                            key="colorGroup_string",
                            match=qdrant_models.MatchValue(value=product_option_id),
                        )
                    ]
                ),
                limit=1,
                with_vectors=True,
                with_payload=False,
            )

            print(f"Found the qdrant ID: {product_option_id} in Qdrant!")
        except Exception as e:
            return f"Error in scrolling: {e}"

        if not scroll_result or not scroll_result[0]:
            raise ValueError(
                f"No vector found for product_option_id = {product_option_id}"
            )

        vector = scroll_result[0][0].vector

        must_conditions = [
            qdrant_models.FieldCondition(key=k, match=qdrant_models.MatchValue(value=v))
            for k, v in (must_filters or {}).items()
        ]

        should_conditions = [
            qdrant_models.FieldCondition(key=k, match=qdrant_models.MatchValue(value=v))
            for k, v in (should_filters or {}).items()
        ]

        query_filter = qdrant_models.Filter(
            must=must_conditions if must_conditions else None,
            should=should_conditions if should_conditions else None,
        )

        search_result = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=limit,
            query_filter=query_filter,
            with_payload=False,
        )

        return [hit.id for hit in search_result]

    def get_qdrant_metadata(
        self,
        point_id: str = None,
        colorGroup_string: str = None,
        required_fields: Union[list, str] = "all",
    ):
        if (not point_id and not colorGroup_string) or (point_id and colorGroup_string):
            print("Searching when both / none cannot happen, exiting")
            return {}

        try:
            id = point_id if point_id else colorGroup_string
            column = "point_id" if point_id else "colorGroup_string"

            print(f"Fetching {column}:{id}")

            scroll_result = self.client.scroll(
                collection_name=COLLECTION_NAME,
                scroll_filter=qdrant_models.Filter(
                    must=[
                        qdrant_models.FieldCondition(
                            key=column,
                            match=qdrant_models.MatchValue(value=id),
                        )
                    ]
                ),
                limit=1,
                with_vectors=False,
                with_payload=True,
            )

            # at most one needs to be matched
            all_results = []
            for res in scroll_result[0]:
                all_results.append(res.payload)

            return all_results

        except Exception as e:
            print(f"Error in fetching qdrant data for id: {id}- {e}")
