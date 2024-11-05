from fastapi import APIRouter

from app.api.api_v1.endpoints import route_auth, route_recipe

api_router = APIRouter()
api_router.include_router(route_auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(route_recipe.router, prefix="/recipes", tags=["Recipes"])


# 'tags' control what appears on OpenAPI heading
# api_router.include_router(route_user.router, prefix="", tags=["User APIs"])
# api_router.include_router(route_blog.router, prefix="", tags=["Blog APIs"])
# api_router.include_router(route_login.router, prefix="", tags=["Login APIs"])
