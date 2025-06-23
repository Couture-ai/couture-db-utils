from pydantic import BaseModel

class SimilarProductsRequest(BaseModel):
    colorGroup_string: str
    dev: dict

class SimilarProductsResponse(BaseModel):
    similar_ids: list
    metadata: dict = {}