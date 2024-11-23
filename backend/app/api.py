from app.deps import get_pinecone, get_meilisearch
from fastapi import Depends, APIRouter
from typing import Optional
from pinecone import Pinecone

from app.helpers import fetch_relevant_vector
from app.schemas import Product
import os
import meilisearch

router = APIRouter(prefix="", tags=["Products"])


@router.get("/products/semantic", response_model=list[Product])
def get_products_by_semantic_search(
    *,
    pinecone_client: Pinecone = Depends(get_pinecone),
    query: Optional[str] = None,
    category_name: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    availability: Optional[str] = None,
):
    filters = {}
    if category_name:
        filters["category_name"] = category_name
    if availability:
        filters["status"] = "IN_STOCK"

    if min_price and not max_price:
        filters["price"] = {"$gte": min_price}

    if max_price and not min_price:
        filters["price"] = {"$lte": max_price}

    if min_price and max_price:
        filters["$and"] = [{"price": {"$gte": min_price}},
                           {"price": {"$lte": max_price}}]

    index = pinecone_client.Index("products")

    result = fetch_relevant_vector(index, query, 100, filters)
    response = []
    data = result.get("matches")
    products_id = []
    scores = 0

    for record in data:
        scores += record.get("score", 0)
    avg_score = scores / 100

    for record in data:
        metadata = record["metadata"]
        pid = int(record["metadata"].get("pid"))
        if pid not in products_id and record.get("score") > avg_score:
            products_id.append(pid)
            response.append(
                Product(
                    id=pid,
                    title=metadata.get("name", ""),
                    images=metadata.get("images", []),
                    price=metadata.get("price", 0),
                )
            )
    return response


@router.get("/products/full-text", response_model=list[Product])
def get_products_by_full_text_search(
    *,
    search_client: meilisearch.Client = Depends(get_meilisearch),
    query: Optional[str] = None,
    category_name: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    availability: Optional[str] = None,
):
    filters = []
    if category_name:
        filters.append(f"category_name = {category_name}")
    if availability:
        filters.append("status = IN_STOCK")

    if min_price:
        filters.append(f"price  >= {min_price}")

    if max_price:
        filters.append(f"price <= {max_price}")

    args = {"attributesToSearchOn": ["name"], "limit": 100}
    f_query = ""
    if filters:
        f_query = " AND ".join(filters)
        args["filter"] = f_query

    index = search_client.index(os.environ.get("MEILISEARCH_INDEX"))

    result = index.search(query, args)
    products = []
    for record in result.get("hits"):
        products.append(
            Product(
                id = record.get("pid"),
                title = record.get("name"),
                images = record.get("images"),
                price = record.get("price"),
            )
        )

    return products
