from pydantic import BaseModel
from typing import Optional, Union


# use the schema from the qdrant schema and construct this
class FiltersRequest(BaseModel):
    brand_string_mv: Optional[str] = None


# Similarity API required models
class SimilarProductsRequest(BaseModel):
    colorGroup_string: str
    product_attributes: Optional[FiltersRequest]
    dev: dict


class SimilarProductsResponse(BaseModel):
    similar_ids: list
    metadata: dict = {}


# QdrantModels
class QdrantSearchRequest(BaseModel):
    colorGroup_string: Optional[str] = None
    point_id: Optional[str] = None
    required_fields: Optional[Union[list, str]] = ["*"]
