from fastapi import APIRouter

from app.api.api_v1.endpoints import route_recipe

api_router = APIRouter()
api_router.include_router(route_recipe.router, prefix="/recipes", tags=["Recipes"])
