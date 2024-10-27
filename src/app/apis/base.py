from apis.v1 import route_blog, route_user
from fastapi import APIRouter

api_router = APIRouter()
# 'tags' control what appears on OpenAPI heading
api_router.include_router(route_user.router, prefix="", tags=["User APIs"])
api_router.include_router(route_blog.router, prefix="", tags=["Blog APIs"])
