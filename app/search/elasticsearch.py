from elasticsearch import AsyncElasticsearch
from app.config import settings

_es_client = None


def get_es() -> AsyncElasticsearch:
    global _es_client
    if _es_client is None:
        _es_client = AsyncElasticsearch([settings.ELASTICSEARCH_URL])
    return _es_client


PRODUCT_INDEX = "products"


async def index_product(product: dict) -> None:
    es = get_es()
    await es.index(index=PRODUCT_INDEX, id=product["id"], body=product)


async def search_products(query: str, page: int = 1, page_size: int = 20) -> dict:
    es = get_es()
    from_offset = (page - 1) * page_size
    body = {
        "from": from_offset,
        "size": page_size,
        "query": {
            "multi_match": {
                "query": query,
                "fields": [
                    "name^3",
                    "description",
                    "tags",
                    "brand.name",
                    "category.name",
                ],
                "fuzziness": "AUTO",
            }
        },
        "sort": [{"_score": {"order": "desc"}}],
    }
    response = await es.search(index=PRODUCT_INDEX, body=body)
    hits = response["hits"]["hits"]
    total = response["hits"]["total"]["value"]
    return {"results": [h["_source"] for h in hits], "total": total}


async def delete_product_from_index(product_id: int) -> None:
    es = get_es()
    await es.delete(index=PRODUCT_INDEX, id=product_id, ignore=[404])
