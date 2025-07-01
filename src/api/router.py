from fastapi import FastAPI, Request, HTTPException
from fastapi.routing import APIRouter
from .pydantic import SimilarProductsRequest, SimilarProductsResponse
import requests

api_router = APIRouter(prefix="/api")

@api_router.post("/similar-products-metadata")
async def get_similar_products_metadata(request: Request, body: SimilarProductsRequest):
    try:
        qdrant_client = request.app.state.qdrant
        redis_client = request.app.state.redis

        similar_ids = qdrant_client.get_similar_product_option_ids(
            product_option_id=body.colorGroup_string
        )

        metadata = {}
        if body.dev.get("metadata", False):
            metadata = await redis_client.fetch_metadata(similar_ids)

        return SimilarProductsResponse(similar_ids=similar_ids, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/search-redirector")
def redirect_to_search(request: Request, query = "Empty"):
    try:
        print(f"Received Query: {query}")
        URL = "http://10.145.4.32:30020/ospreysearch/ajio-search-prevalidation/search-pre-validation"
        input_parameters = {
            "query": query,
            "filters": [],
            "page_number": 1,
            "records_offset": 0,
            "records_per_page": 20,
            "include_unrated_products": True,
            "num_rating_threshold": 0,
            "user_id": "",
            "cohort_id": "",
            "relevance_experiment_field_name": "",
            "store": "rilfnl",
            "catalog_id": "",
            "enable_facet_values_count": True,
            "attributes_to_retrieve": ["*"],
            "facet_columns": [],
            "disable_facets": False,
            "disable_rules": False,
            "enable_stack_trace": False,
        }

        headers = {"api-key": "tDqw3uFTqGddoA.jsDL04dFXqvPsw.AZZaGD7ldj2UkQ"}
        # now send the post request

        result = requests.post(url=URL, json=input_parameters, headers=headers)
        result = result.json()
        return result

    except Exception as e:
        print(f"Exception found in redirecting to Search: {e}")
        return {}
