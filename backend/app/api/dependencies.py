from fastapi import Request

from app.services.elasticsearch_service import ElasticsearchService
from app.services.redis_service import RedisCache


def get_elasticsearch(request: Request) -> ElasticsearchService:
    """Return the Elasticsearch service stored on the FastAPI application."""
    return request.app.state.elasticsearch


def get_cache(request: Request) -> RedisCache:
    """Return the Redis cache stored on the FastAPI application."""
    return request.app.state.cache
